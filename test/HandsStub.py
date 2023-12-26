from src.domain.Hands import Hands, Hand, Joint, Chirality


def should_create_hands():
    return Hands([should_create_hand()])


def should_create_hand() -> Hand:
    return Hand(should_return_knuckles_for_open_hand(), Chirality.RIGHT)


def should_return_knuckles_for_open_hand() -> list[Joint]:
    return [Joint(x=1101, y=735, z=0), Joint(x=973, y=725, z=0), Joint(x=857, y=645, z=0), Joint(x=773, y=573, z=0),
            Joint(x=695, y=530, z=0), Joint(x=932, y=452, z=0), Joint(x=892, y=317, z=0), Joint(x=875, y=220, z=0),
            Joint(x=868, y=141, z=0), Joint(x=1021, y=424, z=0), Joint(x=1011, y=270, z=0), Joint(x=1008, y=164, z=0),
            Joint(x=1009, y=77, z=0), Joint(x=1106, y=432, z=0), Joint(x=1111, y=288, z=0), Joint(x=1115, y=194, z=0),
            Joint(x=1116, y=114, z=0), Joint(x=1186, y=465, z=0), Joint(x=1216, y=360, z=0), Joint(x=1236, y=288, z=0),
            Joint(x=1249, y=221, z=0)]
