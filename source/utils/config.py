import yaml
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Класс для загрузки конфигурационных файлов"""
    
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        
    def parse(self, filename: str) -> Dict[str, Any]:
        """Загрузить конфигурационный файл"""
        filepath = os.path.join(self.config_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Конфигурационный файл не найден: {filepath}")
            
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            logger.info(f"Конфигурация загружена из {filename}")
            return config
        except Exception as e:
            logger.error(f"Ошибка при загрузке конфигурации {filename}: {e}")
            raise
    
    def save_config(self, config: Dict[str, Any], filename: str):
        """Сохранить конфигурацию в файл"""
        filepath = os.path.join(self.config_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            logger.info(f"Конфигурация сохранена в {filename}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении конфигурации {filename}: {e}")
            raise

# Глобальный экземпляр
# ConfigLoader = ConfigLoader()