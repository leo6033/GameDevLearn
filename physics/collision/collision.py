from math import fabs
import utils.math as math


class Sphere(object):
    __slots__ = ['center', 'radius']
    def __init__(self, center: math.Vector3, radius) -> None:
        self.center = center
        self.radius = radius

class AABB(object):
    __slots__ = ['min', 'max']
    def __init__(self, minn: math.Vector2, maxx: math.Vector2) -> None:
        self.min = minn
        self.max = maxx

class Raycast(object):
    __slots__ = ['startPoint', 'endPoint']
    def __init__(self, start: math.Vector3, end: math.Vector3) -> None:
        self.startPoint = start
        self.endPoint = end

class Plane(object):
    __slots__ = ['normal', 'd']
    def __init__(self, normal:math.Vector3, d) -> None:
        self.normal = normal
        self.d = d

class Intersection(object):
    
    @staticmethod
    def SphereIntersection(sphereA: Sphere, sphereB: Sphere):
        # 球与球相交
        v = sphereA.center - sphereB.center
        dis = math.Vector3.dot(v, v)
        return dis < (sphereA.radius + sphereB.radius) ** 2

    @staticmethod
    def AABBIntersection(AABBA: AABB, AABBB: AABB):
        # AABB 包围盒相交
        flag = AABBA.max.x < AABBB.min.x or AABBB.max.x < AABBA.min.x or \
                AABBA.max.y < AABBB.min.y or AABBB.max.y < AABBA.min.y
        return not flag

    @staticmethod
    def LineTriangleIntersection(ray: Raycast, plane: Plane):
        # 射线与平面相交
        v = ray.endPoint - ray.startPoint
        vDotn = math.Vector3.dot(v, plane.normal)
        if fabs(vDotn) > 0.00001:
            t = -1 * (math.Vector3.dot(ray.startPoint, plane.normal) + plane.d)
            t /= vDotn
            return 0 <= t <= 1
        else:
            return math.Vector3.dot(ray.startPoint, plane.normal) + plane.d <= 0.00001
