from random import randint


def num_of_collisions(_num_epoch: int, _num_players: int) -> int:
    def collision() -> bool:
        months = []
        days = []
        for i in range(_num_players):
            months.append(randint(1, 12))  # Random month in interval [1, 12]
            days.append(randint(1, 30))  # Random day in interval [1, 30]

            for j in range(i - 1, -1, -1):
                if months[j] == months[i] and days[j] == days[i]:
                    return True
        return False

    num_collisions = 0
    for _ in range(_num_epoch):
        if collision():
            num_collisions += 1
    return num_collisions


if __name__ == "__main__":
    num_epoch = 1000
    num_players = 23

    probability = num_of_collisions(num_epoch, num_players) / num_epoch
    print(f"Probability for collision is: {probability}")
