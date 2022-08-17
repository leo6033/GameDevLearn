import numpy as np


class Vector2(object):
    __slots__ = ['vec']
    def __init__(self, x=0, y=0) -> None:
        self.vec = np.array([x, y])

    @staticmethod
    def cross(v1, v2):
        result = np.cross(v1.vec, v2.vec)
        return Vector3(0, 0, result)

    @staticmethod
    def dot(v1, v2):
        return np.dot(v1.vec, v2.vec)

    def __sub__(self, other):
        result = Vector2()
        result.vec = self.vec - other.vec
        return result


class Vector3(object):
    __slots__ = ['vec']
    def __init__(self, x=0, y=0, z=0) -> None:
        self.vec = np.array([x, y, z])

    @staticmethod
    def cross(v1, v2):
        result = np.cross(v1.vec, v2.vec)
        return Vector3(result[0], result[1], result[2])
    
    @staticmethod
    def dot(v1, v2):
        return np.dot(v1.vec, v2.vec)

    def __sub__(self, other):
        result = Vector3()
        result.vec = self.vec - other.vec
        return result

v1 = Vector2(1, -1)
v2 = Vector2(1, 1)
print(Vector2.cross(v1, v2).vec)