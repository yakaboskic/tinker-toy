import math

class Part:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _check(self):
        raise NotImplementedError()
    

class Stick(Part):
    orientation_map = {
        0: '|',
        1: '/',
        2: '-',
        3: '\\'
    }

    def __init__(self, x:int, y:int, orientation:int):
        super().__init__(x, y)
        self._check_orientation(orientation)
        self.orientation = orientation

    def _check_orientation(self, orientation):
        if orientation not in [0, 1, 2, 3]:
            raise ValueError(f"Invalid orientation: {orientation}")

class Node(Part):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self.connections = [None for _ in range(8)]

    def join(self, stick, connection):
        # All checks passed, join the stick
        if self._check_stick_connection(stick, connection):
            self.connections[connection] = stick
        return True

    def _check_stick_connection(self, stick, connection):
        # Check for existing connection
        if self.connections[connection]:
            raise ValueError(f"Connection {connection} already occupied")
        # Check for stick location
        dx = stick.x - self.x
        dy = stick.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > math.sqrt(2):
            raise ValueError(f"Stick too far away")
        # Check for stick orientation and allowed connection point
        if dx == 0:
            if stick.orientation != 0:
                raise ValueError(f"Invalid orientation for vertical stick")
            if dy > 0 and connection != 0:
                raise ValueError(f"Invalid connection for vertical stick at {dx}, {dy}")
            if dy < 0 and connection != 4:
                raise ValueError(f"Invalid connection for vertical stick at {dx}, {dy}")
        if dy == 0:
            if stick.orientation != 2:
                raise ValueError(f"Invalid orientation for horizontal stick")
            if dx > 0 and connection != 2:
                raise ValueError(f"Invalid connection for horizontal stick at {dx}, {dy}")
            if dx < 0 and connection != 6:
                raise ValueError(f"Invalid connection for horizontal stick at {dx}, {dy}")
        if dx != 0 and dy != 0:
            if dx == dy:
                if stick.orientation != 1:
                    raise ValueError(f"Invalid orientation for diagonal stick")
                if dx > 0 and connection != 1:
                    raise ValueError(f"Invalid orientation for diagonal stick at {dx}, {dy}")
                if dx < 0 and connection != 5:
                    raise ValueError(f"Invalid orientation for diagonal stick at {dx}, {dy}")
            elif dx == -dy:
                if stick.orientation != 3:
                    raise ValueError(f"Invalid orientation for diagonal stick")
                if dx > dy and connection != 3:
                    raise ValueError(f"Invalid orientation for diagonal stick at {dx}, {dy}")
                if dx < dy and connection != 7:
                    raise ValueError(f"Invalid orientation for diagonal stick at {dx}, {dy}")
        return True
    

class World:
    def __init__(self, height:int, width:int):
        self.height = height
        self.width = width
        self.parts = []

    def add_stick(self, x:int, y:int, orientation:int):
        stick = Stick(x, y, orientation)
        self.parts.append(stick)
        return stick

    def add_node(self, x:int, y:int):
        node = Node(x, y)
        self.parts.append(node)
        return node

    def connect(self, stick, node, connection):
        return node.join(stick, connection)    