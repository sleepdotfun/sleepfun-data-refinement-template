from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class TemperatureData(BaseModel):
    delta: Optional[float] = None


class ReadinessData(BaseModel):
    readiness: Optional[float] = None
    recovery_level: Optional[int] = None


class AwakeData(BaseModel):
    wake_up_latency_seconds: Optional[float] = None
    duration_short_interruption_seconds: Optional[float] = None
    num_out_of_bed_events: Optional[int] = None
    duration_awake_state_seconds: Optional[float] = None
    num_wakeup_events: Optional[int] = None
    duration_long_interruption_seconds: Optional[float] = None
    sleep_latency_seconds: Optional[float] = None


class AsleepData(BaseModel):
    num_REM_events: Optional[int] = None
    duration_asleep_state_seconds: Optional[float] = None
    duration_light_sleep_state_seconds: Optional[float] = None
    duration_deep_sleep_state_seconds: Optional[float] = None
    duration_REM_sleep_state_seconds: Optional[float] = None


class OtherSleepData(BaseModel):
    duration_unmeasurable_sleep_seconds: Optional[float] = None
    duration_in_bed_seconds: Optional[float] = None


class SleepDurationsData(BaseModel):
    awake: AwakeData
    asleep: AsleepData
    sleep_efficiency: Optional[float] = None
    hypnogram_samples: List[float] = []
    other: OtherSleepData


class Metadata(BaseModel):
    timestamp_localization: Optional[int] = None
    summary_id: Optional[str] = None
    upload_type: Optional[int] = None
    end_time: Optional[datetime] = None
    is_nap: Optional[bool] = None
    start_time: Optional[datetime] = None


class DataEnrichment(BaseModel):
    sleep_score: Optional[float] = None
    sleep_contributors: Optional[dict] = None


class HeartRateSummary(BaseModel):
    max_hr_bpm: Optional[float] = None
    user_max_hr_bpm: Optional[float] = None
    avg_hrv_sdnn: Optional[float] = None
    resting_hr_bpm: Optional[float] = None
    avg_hr_bpm: Optional[float] = None
    avg_hrv_rmssd: Optional[float] = None
    min_hr_bpm: Optional[float] = None


class HeartRateDetailed(BaseModel):
    hr_samples: List[float] = []
    hrv_samples_rmssd: List[float] = []
    hrv_samples_sdnn: List[float] = []


class HeartRateData(BaseModel):
    summary: HeartRateSummary
    detailed: HeartRateDetailed


class Scores(BaseModel):
    sleep: Optional[float] = None


class OxygenSaturationData(BaseModel):
    samples: List[float] = []
    end_time: Optional[datetime] = None
    avg_saturation_percentage: Optional[float] = None
    start_time: Optional[datetime] = None


class SnoringData(BaseModel):
    samples: List[float] = []
    end_time: Optional[datetime] = None
    num_snoring_events: Optional[int] = None
    total_snoring_duration_seconds: Optional[float] = None
    start_time: Optional[datetime] = None


class BreathsData(BaseModel):
    samples: List[float] = []
    end_time: Optional[datetime] = None
    max_breaths_per_min: Optional[float] = None
    on_demand_reading: Optional[bool] = None
    avg_breaths_per_min: Optional[float] = None
    min_breaths_per_min: Optional[float] = None
    start_time: Optional[datetime] = None


class RespirationData(BaseModel):
    oxygen_saturation_data: OxygenSaturationData
    snoring_data: SnoringData
    breaths_data: BreathsData


class DeviceData(BaseModel):
    name: Optional[str] = None
    last_upload_date: Optional[datetime] = None
    software_version: Optional[str] = None
    serial_number: Optional[str] = None
    hardware_version: Optional[str] = None
    activation_timestamp: Optional[datetime] = None
    other_devices: List[str] = []
    manufacturer: Optional[str] = None
    data_provided: List[str] = []


class User(BaseModel):
    reference_id: Optional[str] = None
    last_webhook_update: Optional[datetime] = None
    active: Optional[bool] = None
    scopes: Optional[str] = None
    provider: Optional[str] = None
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    age: Optional[int] = None


class SleepData(BaseModel):
    temperature_data: TemperatureData
    readiness_data: ReadinessData
    sleep_durations_data: SleepDurationsData
    metadata: Metadata
    data_enrichment: DataEnrichment
    heart_rate_data: HeartRateData
    scores: Scores
    respiration_data: RespirationData
    device_data: DeviceData
    user: User 