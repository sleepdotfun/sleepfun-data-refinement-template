from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TemperatureRefined(Base):
    __tablename__ = 'temperatures'
    
    temperature_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_id = Column(String, ForeignKey('sleep_records.sleep_id'), nullable=False)
    delta = Column(Float, nullable=True)
    
    sleep_record = relationship("SleepRefined", back_populates="temperature_data")

class ReadinessRefined(Base):
    __tablename__ = 'readiness'
    
    readiness_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_id = Column(String, ForeignKey('sleep_records.sleep_id'), nullable=False)
    readiness = Column(Float, nullable=True)
    recovery_level = Column(Integer, nullable=True)
    
    sleep_record = relationship("SleepRefined", back_populates="readiness_data")

class AwakeRefined(Base):
    __tablename__ = 'awake_periods'
    
    awake_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_duration_id = Column(Integer, ForeignKey('sleep_durations.duration_id'), nullable=False)
    wake_up_latency_seconds = Column(Float, nullable=True)
    duration_short_interruption_seconds = Column(Float, nullable=True)
    num_out_of_bed_events = Column(Integer, nullable=True)
    duration_awake_state_seconds = Column(Float, nullable=True)
    num_wakeup_events = Column(Integer, nullable=True)
    duration_long_interruption_seconds = Column(Float, nullable=True)
    sleep_latency_seconds = Column(Float, nullable=True)
    
    sleep_duration = relationship("SleepDurationRefined", back_populates="awake")

class AsleepRefined(Base):
    __tablename__ = 'asleep_periods'
    
    asleep_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_duration_id = Column(Integer, ForeignKey('sleep_durations.duration_id'), nullable=False)
    num_REM_events = Column(Integer, nullable=True)
    duration_asleep_state_seconds = Column(Float, nullable=True)
    duration_light_sleep_state_seconds = Column(Float, nullable=True)
    duration_deep_sleep_state_seconds = Column(Float, nullable=True)
    duration_REM_sleep_state_seconds = Column(Float, nullable=True)
    
    sleep_duration = relationship("SleepDurationRefined", back_populates="asleep")

class SleepDurationRefined(Base):
    __tablename__ = 'sleep_durations'
    
    duration_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_id = Column(String, ForeignKey('sleep_records.sleep_id'), nullable=False)
    sleep_efficiency = Column(Float, nullable=True)
    hypnogram_samples = Column(JSON, nullable=True)
    duration_unmeasurable_sleep_seconds = Column(Float, nullable=True)
    duration_in_bed_seconds = Column(Float, nullable=True)
    
    sleep_record = relationship("SleepRefined", back_populates="sleep_durations_data")
    awake = relationship("AwakeRefined", uselist=False, back_populates="sleep_duration")
    asleep = relationship("AsleepRefined", uselist=False, back_populates="sleep_duration")

class HeartRateSummaryRefined(Base):
    __tablename__ = 'heart_rate_summaries'
    
    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    heart_rate_id = Column(Integer, ForeignKey('heart_rates.heart_rate_id'), nullable=False)
    max_hr_bpm = Column(Float, nullable=True)
    user_max_hr_bpm = Column(Float, nullable=True)
    avg_hrv_sdnn = Column(Float, nullable=True)
    resting_hr_bpm = Column(Float, nullable=True)
    avg_hr_bpm = Column(Float, nullable=True)
    avg_hrv_rmssd = Column(Float, nullable=True)
    min_hr_bpm = Column(Float, nullable=True)
    
    heart_rate = relationship("HeartRateRefined", back_populates="summary")

class HeartRateDetailedRefined(Base):
    __tablename__ = 'heart_rate_details'
    
    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    heart_rate_id = Column(Integer, ForeignKey('heart_rates.heart_rate_id'), nullable=False)
    hr_samples = Column(JSON, nullable=True)
    hrv_samples_rmssd = Column(JSON, nullable=True)
    hrv_samples_sdnn = Column(JSON, nullable=True)
    
    heart_rate = relationship("HeartRateRefined", back_populates="detailed")

class HeartRateRefined(Base):
    __tablename__ = 'heart_rates'
    
    heart_rate_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_id = Column(String, ForeignKey('sleep_records.sleep_id'), nullable=False)
    
    sleep_record = relationship("SleepRefined", back_populates="heart_rate_data")
    summary = relationship("HeartRateSummaryRefined", uselist=False, back_populates="heart_rate")
    detailed = relationship("HeartRateDetailedRefined", uselist=False, back_populates="heart_rate")

class RespirationRefined(Base):
    __tablename__ = 'respirations'
    
    respiration_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_id = Column(String, ForeignKey('sleep_records.sleep_id'), nullable=False)
    
    sleep_record = relationship("SleepRefined", back_populates="respiration_data")
    oxygen_data = relationship("OxygenSaturationRefined", uselist=False, back_populates="respiration")
    snoring_data = relationship("SnoringRefined", uselist=False, back_populates="respiration")
    breaths_data = relationship("BreathsRefined", uselist=False, back_populates="respiration")

class OxygenSaturationRefined(Base):
    __tablename__ = 'oxygen_saturations'
    
    oxygen_id = Column(Integer, primary_key=True, autoincrement=True)
    respiration_id = Column(Integer, ForeignKey('respirations.respiration_id'), nullable=False)
    samples = Column(JSON, nullable=True)
    end_time = Column(DateTime, nullable=True)
    avg_saturation_percentage = Column(Float, nullable=True)
    start_time = Column(DateTime, nullable=True)
    
    respiration = relationship("RespirationRefined", back_populates="oxygen_data")

class SnoringRefined(Base):
    __tablename__ = 'snoring'
    
    snoring_id = Column(Integer, primary_key=True, autoincrement=True)
    respiration_id = Column(Integer, ForeignKey('respirations.respiration_id'), nullable=False)
    samples = Column(JSON, nullable=True)
    end_time = Column(DateTime, nullable=True)
    num_snoring_events = Column(Integer, nullable=True)
    total_snoring_duration_seconds = Column(Float, nullable=True)
    start_time = Column(DateTime, nullable=True)
    
    respiration = relationship("RespirationRefined", back_populates="snoring_data")

class BreathsRefined(Base):
    __tablename__ = 'breaths'
    
    breath_id = Column(Integer, primary_key=True, autoincrement=True)
    respiration_id = Column(Integer, ForeignKey('respirations.respiration_id'), nullable=False)
    samples = Column(JSON, nullable=True)
    end_time = Column(DateTime, nullable=True)
    max_breaths_per_min = Column(Float, nullable=True)
    on_demand_reading = Column(Boolean, nullable=True)
    avg_breaths_per_min = Column(Float, nullable=True)
    min_breaths_per_min = Column(Float, nullable=True)
    start_time = Column(DateTime, nullable=True)
    
    respiration = relationship("RespirationRefined", back_populates="breaths_data")

class DeviceRefined(Base):
    __tablename__ = 'devices'
    
    device_id = Column(Integer, primary_key=True, autoincrement=True)
    sleep_id = Column(String, ForeignKey('sleep_records.sleep_id'), nullable=False)
    name = Column(String, nullable=True)
    last_upload_date = Column(DateTime, nullable=True)
    software_version = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    hardware_version = Column(String, nullable=True)
    activation_timestamp = Column(DateTime, nullable=True)
    other_devices = Column(JSON, nullable=True)
    manufacturer = Column(String, nullable=True)
    data_provided = Column(JSON, nullable=True)
    
    sleep_record = relationship("SleepRefined", back_populates="device_data")

class UserRefined(Base):
    __tablename__ = 'users'
    
    user_id = Column(String, primary_key=True)
    reference_id = Column(String, nullable=True)
    last_webhook_update = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True)
    scopes = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    age = Column(Integer, nullable=True)
    
    sleep_records = relationship("SleepRefined", back_populates="user")

class SleepRefined(Base):
    __tablename__ = 'sleep_records'
    
    sleep_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    sleep_score = Column(Float, nullable=True)
    
    user = relationship("UserRefined", back_populates="sleep_records")
    temperature_data = relationship("TemperatureRefined", uselist=False, back_populates="sleep_record")
    readiness_data = relationship("ReadinessRefined", uselist=False, back_populates="sleep_record")
    sleep_durations_data = relationship("SleepDurationRefined", uselist=False, back_populates="sleep_record")
    heart_rate_data = relationship("HeartRateRefined", uselist=False, back_populates="sleep_record")
    respiration_data = relationship("RespirationRefined", uselist=False, back_populates="sleep_record")
    device_data = relationship("DeviceRefined", uselist=False, back_populates="sleep_record") 