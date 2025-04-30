import sys
import json
import logging
import traceback
import shutil
import zipfile
from pathlib import Path
from supabase import create_client, Client
from pydantic_settings import BaseSettings
from pydantic import Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

OUTPUT_DIR = "./download-sleep-data/output"

# If limit is set, only download the X latest payload.
# if 0, download ALL payloads
LIMIT = 0

class Settings(BaseSettings):
    """Global settings configuration using environment variables"""
    
    SUPABASE_URL: str = Field(
        description="Supabase project URL"
    )
    
    SUPABASE_ANON_KEY: str = Field(
        description="Supabase anonymous key"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow additional fields

settings = Settings()

# Initialize Supabase client
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_ANON_KEY
)

async def download_sleep_payload(payload_id: str, output_path: Path) -> bool:
    """Download a single sleep payload from Supabase storage and save to file."""
    try:
        response = supabase.storage.from_('terra-payloads').download(f'sleep/{payload_id}.json')
        if response:
            # Create output file
            output_file = output_path / f"{payload_id}.json"
            with open(output_file, 'w') as f:
                data = json.loads(response.decode('utf-8'))
                data['id'] = payload_id
                json.dump(data, f, indent=2)
            return True
        return False
    except Exception as e:
        logging.error(f"Error downloading payload {payload_id}: {e}")
        return False

async def get_all_payload_ids() -> list[str]:
    """Get a list of all sleep payload IDs from the terra_data_payloads table."""
    try:
        all_payload_ids = []
        page_size = 1000  # Supabase has a default limit of 1000 records per query
        offset = 0
        
        while True:
            query = supabase.table('terra_data_payloads').select('payload_id').eq('data_type', 'sleep').order('created_at', desc=True).range(offset, offset + page_size - 1)
            if LIMIT > 0 and offset + page_size > LIMIT:
                # If we're about to exceed the user-defined limit, adjust the page size
                query = query.limit(LIMIT - offset)
            
            response = query.execute()
            
            if not response or not response.data or len(response.data) == 0:
                break
                
            all_payload_ids.extend([item['payload_id'] for item in response.data])
            
            # If we've reached the user-defined limit or received fewer records than page_size, we're done
            if (LIMIT > 0 and len(all_payload_ids) >= LIMIT) or len(response.data) < page_size:
                break
                
            offset += page_size
            
            # If we have a user-defined limit, make sure we don't fetch more than needed
            if LIMIT > 0 and offset >= LIMIT:
                break
                
        return all_payload_ids
    except Exception as e:
        logging.error(f"Error getting payload IDs from database: {e}")
        return []

def create_zip_file(temp_dir: Path, output_dir: Path) -> bool:
    """Create a zip file from the temp directory and delete the temp directory."""
    try:
        zip_path = output_dir / "user.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in temp_dir.rglob('*'):
                if file.is_file():
                    zipf.write(file, file.relative_to(temp_dir))
        
        # Delete temp directory
        shutil.rmtree(temp_dir)
        return True
    except Exception as e:
        logging.error(f"Error creating zip file: {e}")
        return False

async def run():
    """Main function to download all sleep payloads."""
    # Create output and temp directories
    output_dir = Path(OUTPUT_DIR)
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all payload IDs
    payload_ids = await get_all_payload_ids()
    logging.info(f"Found {len(payload_ids)} sleep payloads to download")
    
    # Download each payload
    success_count = 0
    for payload_id in payload_ids:
        if await download_sleep_payload(payload_id, temp_dir):
            success_count += 1
            logging.info(f"Successfully downloaded payload {payload_id}")
        else:
            logging.warning(f"Failed to download payload {payload_id}")
    
    # Create zip file and clean up
    if success_count > 0:
        if create_zip_file(temp_dir, output_dir):
            logging.info(f"Successfully created zip file with {success_count} payloads")
        else:
            logging.error("Failed to create zip file")
    else:
        logging.warning("No payloads were downloaded successfully")
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(run())
    except Exception as e:
        logging.error(f"Error during data transformation: {e}")
        traceback.print_exc()
        sys.exit(1)
