import os
import logging
import polars as pl
from typing import List, Dict, Any, Optional
from multipledispatch import dispatch


logger = logging.getLogger(__name__)

class FeaturesManager:

    def __init__(
        self,
        num: List[str],
        cat: List[str],
        target: str
    ):
        """
        Инициализирует объект с данными и метаинформацией о признаках.

        Args:
            data (pl.DataFrame): Таблица данных типа polars DataFrame. 
            num (List[str]): Список названий числовых признаков.
            cat (List[str]): Список названий категориальных признаков.
            target (str): Название целевого признака.
        """

        self._numerical: List = num
        self._categorical: List = cat
        self._target: str = target

    @property
    def X(self) -> List[str]:
        """
        Returns:
            List[str]: Список наименования признаков
        """
        return self._numerical.copy() + self._categorical.copy()


    @property
    def Y(self) -> str:
        """    
        Returns:
            str: Наименование целевой переменной
        """
        return self._target


    @property
    def XY(self) -> List[str]:
        """    
        Returns:
            List[str]: Наименование целевой переменной
        """

        _XY = self.X
        _XY.append(self.Y)
        return _XY


    @property
    def numerical(self) -> List[str]:
        """    
        Returns:
            List[str]: Возвращает список названий категориальных признаков.
        """
        return self._numerical.copy()


    @property
    def categorical(self) -> List[str]:
        """    
        Returns:
            List[str]: Список названий категориальных признаков.
        """
        return self._categorical.copy()
    

    def numerical_idx(self, data: pl.DataFrame) -> List[float]:
        """
        Returns:
            List[float]: Список индексов числовых признаков
        """
        return [data.get_column_index(name) for name in self._numerical]

 
    def categorical_idx(self, data: pl.DataFrame) -> List[float]:
        """
        Returns:
            List[float]: Список индексов категориальных признаков.
        """
        return [data.get_column_index(name) for name in self._categorical]
    

    def add(self, value: str, type_feature: str) -> None:
        '''
        Добавляет новое имя признака в список.

        Метод регистрирует признак с указанным именем и типом в внутреннем хранилище.

        Args:
            value (str): Уникальное название признака. Не должно быть пустым.
            type_feature (str): Тип признака. Должен принимать одно из значений:
                - "num": Числовой признак (например, возраст, доход).
                - "cat": Категориальный признак (например, пол, категория товара).

        Raises:
            ValueError: Если `type_feature` не равен "num" или "cat".

        Returns:
            None: Метод не возвращает значение.
        '''
        # Проверка типов
        if not isinstance(value, str):
            raise TypeError(f"Параметр 'value' должен быть строкой, получено: {type(value).__name__}")
        
        if not isinstance(type_feature, str):
            raise TypeError(f"Параметр 'type_feature' должен быть строкой, получено: {type(type_feature).__name__}")

        # Проверка на пустоту
        if not value or not value.strip():
            raise ValueError("Параметр 'value' не может быть пустым или состоять только из пробелов")

        # Проверка допустимых значений type_feature
        if type_feature not in ("num", "cat"):
            raise ValueError(
                f"Параметр 'type_feature' должен быть 'num' или 'cat', получено: '{type_feature}'"
            )
        
        if type_feature == "num" and not value in self._numerical:
            self._numerical.append(value)
            return
        
        if type_feature == "cat" and not value in self._categorical:
            self._categorical.append(value)
            return


    @dispatch(str)
    def remove(self, col: str) -> None:
        """
        Удаляет один признак из соответствующих списков.
        
        Args:
            col (str): Название признака для удаления.

        Returns:
            None

        Example:
            manager.remove('age')
        """
        try:
            if col in self._categorical:
                self._categorical.remove(col)
            else:
                self._numerical.remove(col)
        except ValueError as e:
            raise ValueError(f"FeatureManager не содержит {col} признак!") from e


    @dispatch(list)
    def remove(self, cols: List[str])  -> None:
        """
        Удаляет несколько признаков из списков.
        
        Args:
            cols (List[str]): Список названий признаков.

        Returns:
            None

        Example:
            manager.remove(['age', 'gender'])
        """
        for col in cols:
            try:
                if col in self._categorical:
                    self._categorical.remove(col)
                else:
                    self._numerical.remove(col)
            except ValueError as e:
                raise ValueError(f"FeatureManager не содержит {col} признак!") from e
