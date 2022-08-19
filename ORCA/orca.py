import math
import utils.math as umath

class Line(object):
	def __init__(self, point, dir):
		super(Line, object).__init__()
		self.point = point
		self.dir = dir

class ORCAAgent(object):
	def __init__(self, position, radius, velocity, max_speed):
		super(ORCAAgent, self).__init__()
		self.position = position
		self.radius = radius
		self.velocity = velocity
		self.ori_velocity = velocity
		self.max_speed = max_speed

class ORCA(object):
	def __init__(self, agent):
		super(ORCA, self).__init__()
		self.agent = agent
		self.other_angets = []
		self.line_chache = []
	
	def add_agent(self, agent):
		if isinstance(agent, ORCAAgent):
			self.other_angets.append(agent)
		else:
			print "only orca agent can be added"

	def calc(self, t, dt):
		lines = []
		for agent in self.other_angets:
			u, n = self.get_avoidance_velocity(agent, t, dt)
			line = Line(u, n)
			lines.append(line)
		return self.halfplane_optimize(lines)
	
	def get_avoidance_velocity(self, collider_agent, t, dt):
		""" calculate VO """
		# PB - PA
		x = collider_agent.position - self.agent.position
		# B 为参考系下 A 的速度
		v = self.agent.velocity - collider_agent.velocity
		# RA + RB
		r = self.agent.radius + collider_agent.radius

		x_len_sq = x.dot(x)
		if x_len_sq > r * r:
			adjusted_center = x.div(t)
			u = -x.normalize()
			cos_theta = r / math.sqrt(x_len_sq)
			cv = v - adjusted_center
			if cv.dot(u) < cv.dot(cv) * cos_theta:
				# 顶部扇形区域内
				w = cv
				u = (cv.normalize() * r).div(t) - w
				n = w.normalize()
			else:
				leg_len = math.sqrt(x_len_sq - r * r)
				sine = math.copysign(r, v.det(x))
				rot1 = umath.Vector2(leg_len, sine)
				rot2 = umath.Vector2(-sine, leg_len)
				rotated_x = umath.Vector2(rot1.dot(x), rot2.dot(x))
				rotated_x = rotated_x.div(x_len_sq)
				n = rotated_x.perp()
				if sine < 0:
					n = -n
				u = rotated_x * v.dot(rotated_x) - v
		else:
			w = v - x.div(dt)
			u = (w.normalize() * r).div(dt) - w
			n = w.normalize()
	
	def halfplane_optimize(self, lines):
		point = self.agent.velocity
		for idx, line in enumerate(lines):
			if (point - line.point).dot(line.direction) >= 0:
				continue
			ret, left_dist, right_dist = self.line_halfplane_intersect(line, lines, idx)
			if not ret:
				return umath.Vector2(0, 0)
			point = self.point_line_project(line, self.agent.velocity, left_dist, right_dist)
		return point
	
	def line_halfplane_intersect(self, line, lines, idx):
		left_dist = -math.inf
		right_dist = math.inf
		for i in xrange(idx):
			prev_line = lines[i]
			num = prev_line.direction.dot(line.point - prev_line.point)
			den = line.direction.det(prev_line.direction)

			if den == 0:
				if num < 0:
					return False, left_dist, right_dist
				else:
					continue
			
			offset = num / den
			if den > 0:
				right_dist = min(right_dist, offset)
			else:
				left_dist = max(left_dist, offset)
			
			if left_dist > right_dist:
				return False, left_dist, right_dist
			
		return True, left_dist, right_dist
	
	def point_line_project(self, line, point, left_dist, right_dist):
		new_dir = line.directino.perp()
		proj_len = (point - line.point).dot(new_dir)
		clamped_len = min(max(proj_len, left_dist), right_dist)
		return line.point + new_dir + clamped_len
