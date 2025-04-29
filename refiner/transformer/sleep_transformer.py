from typing import Dict, Any, List
from datetime import datetime
from refiner.models.refined import Base
from refiner.transformer.base_transformer import DataTransformer
from refiner.models.refined import (
    UserRefined, SleepRefined, TemperatureRefined, ReadinessRefined,
    AwakeRefined, AsleepRefined, SleepDurationRefined,
    HeartRateRefined, HeartRateSummaryRefined, HeartRateDetailedRefined,
    RespirationRefined, OxygenSaturationRefined, SnoringRefined, BreathsRefined,
    DeviceRefined
)
from refiner.models.unrefined import SleepData

class SleepTransformer(DataTransformer):
    """
    Transformer for sleep data from various health tracking devices.
    Handles the complex nested structure of sleep records and their associated metrics.
    """
    
    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw sleep data into SQLAlchemy model instances.
        
        Args:
            data: Dictionary containing sleep tracking data
            
        Returns:
            List of SQLAlchemy model instances
        """
        # Validate data with Pydantic
        unrefined_data = SleepData.model_validate(data)
        models = []
        
        # Create user
        user = UserRefined(
            user_id=unrefined_data.user.user_id,
            reference_id=unrefined_data.user.reference_id,
            last_webhook_update=unrefined_data.user.last_webhook_update,
            active=unrefined_data.user.active,
            scopes=unrefined_data.user.scopes,
            provider=unrefined_data.user.provider,
            created_at=unrefined_data.user.created_at,
            age=unrefined_data.user.age
        )
        models.append(user)
        
        # Create sleep record
        sleep_record = SleepRefined(
            sleep_id=unrefined_data.id,
            user_id=user.user_id,
            sleep_score=unrefined_data.data_enrichment.sleep_score
        )
        models.append(sleep_record)
        
        # Temperature data
        if unrefined_data.temperature_data:
            temp = TemperatureRefined(
                sleep_id=sleep_record.sleep_id,
                delta=unrefined_data.temperature_data.delta
            )
            models.append(temp)
        
        # Readiness data
        if unrefined_data.readiness_data:
            readiness = ReadinessRefined(
                sleep_id=sleep_record.sleep_id,
                readiness=unrefined_data.readiness_data.readiness,
                recovery_level=unrefined_data.readiness_data.recovery_level
            )
            models.append(readiness)
        
        # Sleep duration data
        if unrefined_data.sleep_durations_data:
            duration = SleepDurationRefined(
                sleep_id=sleep_record.sleep_id,
                sleep_efficiency=unrefined_data.sleep_durations_data.sleep_efficiency,
                hypnogram_samples=unrefined_data.sleep_durations_data.hypnogram_samples,
                duration_unmeasurable_sleep_seconds=unrefined_data.sleep_durations_data.other.duration_unmeasurable_sleep_seconds,
                duration_in_bed_seconds=unrefined_data.sleep_durations_data.other.duration_in_bed_seconds
            )
            models.append(duration)
            
            # Awake data
            if unrefined_data.sleep_durations_data.awake:
                awake = AwakeRefined(
                    sleep_duration=duration,  # Use relationship instead of ID
                    wake_up_latency_seconds=unrefined_data.sleep_durations_data.awake.wake_up_latency_seconds,
                    duration_short_interruption_seconds=unrefined_data.sleep_durations_data.awake.duration_short_interruption_seconds,
                    num_out_of_bed_events=unrefined_data.sleep_durations_data.awake.num_out_of_bed_events,
                    duration_awake_state_seconds=unrefined_data.sleep_durations_data.awake.duration_awake_state_seconds,
                    num_wakeup_events=unrefined_data.sleep_durations_data.awake.num_wakeup_events,
                    duration_long_interruption_seconds=unrefined_data.sleep_durations_data.awake.duration_long_interruption_seconds,
                    sleep_latency_seconds=unrefined_data.sleep_durations_data.awake.sleep_latency_seconds
                )
                models.append(awake)
            
            # Asleep data
            if unrefined_data.sleep_durations_data.asleep:
                asleep = AsleepRefined(
                    sleep_duration=duration,  # Use relationship instead of ID
                    num_REM_events=unrefined_data.sleep_durations_data.asleep.num_REM_events,
                    duration_asleep_state_seconds=unrefined_data.sleep_durations_data.asleep.duration_asleep_state_seconds,
                    duration_light_sleep_state_seconds=unrefined_data.sleep_durations_data.asleep.duration_light_sleep_state_seconds,
                    duration_deep_sleep_state_seconds=unrefined_data.sleep_durations_data.asleep.duration_deep_sleep_state_seconds,
                    duration_REM_sleep_state_seconds=unrefined_data.sleep_durations_data.asleep.duration_REM_sleep_state_seconds
                )
                models.append(asleep)
        
        # Heart rate data
        if unrefined_data.heart_rate_data:
            heart_rate = HeartRateRefined(
                sleep_id=sleep_record.sleep_id
            )
            models.append(heart_rate)
            
            # Summary
            if unrefined_data.heart_rate_data.summary:
                summary = HeartRateSummaryRefined(
                    heart_rate=heart_rate,  # Use relationship instead of ID
                    max_hr_bpm=unrefined_data.heart_rate_data.summary.max_hr_bpm,
                    user_max_hr_bpm=unrefined_data.heart_rate_data.summary.user_max_hr_bpm,
                    avg_hrv_sdnn=unrefined_data.heart_rate_data.summary.avg_hrv_sdnn,
                    resting_hr_bpm=unrefined_data.heart_rate_data.summary.resting_hr_bpm,
                    avg_hr_bpm=unrefined_data.heart_rate_data.summary.avg_hr_bpm,
                    avg_hrv_rmssd=unrefined_data.heart_rate_data.summary.avg_hrv_rmssd,
                    min_hr_bpm=unrefined_data.heart_rate_data.summary.min_hr_bpm
                )
                models.append(summary)
            
            # Detailed
            if unrefined_data.heart_rate_data.detailed:
                detailed = HeartRateDetailedRefined(
                    heart_rate=heart_rate,  # Use relationship instead of ID
                    hr_samples=unrefined_data.heart_rate_data.detailed.hr_samples,
                    hrv_samples_rmssd=unrefined_data.heart_rate_data.detailed.hrv_samples_rmssd,
                    hrv_samples_sdnn=unrefined_data.heart_rate_data.detailed.hrv_samples_sdnn
                )
                models.append(detailed)
        
        # Respiration data
        if unrefined_data.respiration_data:
            respiration = RespirationRefined(
                sleep_id=sleep_record.sleep_id
            )
            models.append(respiration)
            
            # Oxygen saturation
            if unrefined_data.respiration_data.oxygen_saturation_data:
                oxygen = OxygenSaturationRefined(
                    respiration=respiration,  # Use relationship instead of ID
                    samples=unrefined_data.respiration_data.oxygen_saturation_data.samples,
                    end_time=unrefined_data.respiration_data.oxygen_saturation_data.end_time,
                    avg_saturation_percentage=unrefined_data.respiration_data.oxygen_saturation_data.avg_saturation_percentage,
                    start_time=unrefined_data.respiration_data.oxygen_saturation_data.start_time
                )
                models.append(oxygen)
            
            # Snoring
            if unrefined_data.respiration_data.snoring_data:
                snoring = SnoringRefined(
                    respiration=respiration,  # Use relationship instead of ID
                    samples=unrefined_data.respiration_data.snoring_data.samples,
                    end_time=unrefined_data.respiration_data.snoring_data.end_time,
                    num_snoring_events=unrefined_data.respiration_data.snoring_data.num_snoring_events,
                    total_snoring_duration_seconds=unrefined_data.respiration_data.snoring_data.total_snoring_duration_seconds,
                    start_time=unrefined_data.respiration_data.snoring_data.start_time
                )
                models.append(snoring)
            
            # Breaths
            if unrefined_data.respiration_data.breaths_data:
                breaths = BreathsRefined(
                    respiration=respiration,  # Use relationship instead of ID
                    samples=unrefined_data.respiration_data.breaths_data.samples,
                    end_time=unrefined_data.respiration_data.breaths_data.end_time,
                    max_breaths_per_min=unrefined_data.respiration_data.breaths_data.max_breaths_per_min,
                    on_demand_reading=unrefined_data.respiration_data.breaths_data.on_demand_reading,
                    avg_breaths_per_min=unrefined_data.respiration_data.breaths_data.avg_breaths_per_min,
                    min_breaths_per_min=unrefined_data.respiration_data.breaths_data.min_breaths_per_min,
                    start_time=unrefined_data.respiration_data.breaths_data.start_time
                )
                models.append(breaths)
        
        # Device data
        if unrefined_data.device_data:
            device = DeviceRefined(
                sleep_id=sleep_record.sleep_id,
                name=unrefined_data.device_data.name,
                last_upload_date=unrefined_data.device_data.last_upload_date,
                software_version=unrefined_data.device_data.software_version,
                serial_number=unrefined_data.device_data.serial_number,
                hardware_version=unrefined_data.device_data.hardware_version,
                activation_timestamp=unrefined_data.device_data.activation_timestamp,
                other_devices=unrefined_data.device_data.other_devices,
                manufacturer=unrefined_data.device_data.manufacturer,
                data_provided=unrefined_data.device_data.data_provided
            )
            models.append(device)
        
        return models 