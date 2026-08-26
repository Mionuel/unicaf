from pydantic import BaseModel

class SimulationSettings(BaseModel):
    # app.py
    simulation_interval: float = 0.1
    
    # queue_controller.py
    max_queue_size: int = 25
    
    # seat_controller.py
    occupy_seconds_min: int = 30
    occupy_seconds_variance: int = 20
    occupy_seconds_snack: int = 30
    order_cost: float = 5.0
    
    # person_controller.py
    bonus_threshold: int = 5

    # simulation_controller.py
    update_delay: float = 0.2

# Global instance of settings
app_settings = SimulationSettings()
