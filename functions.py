def clean_screen():
    print("\n" * 30)


def print_grid(own_grid, rival_grid, low_line, message=""):

    rival_grid = rival_grid.copy()
    for square in rival_grid:
        if rival_grid[square] == "■":
            rival_grid[square] = "-"

    clean_screen()
    print("  ⚓ ПОЛЕ ПРОТИВНИКА ⚓    ⚓   ВАШЕ ПОЛЕ   ⚓")
    print("    А  Б  В  Г  Д  Е         А  Б  В  Г  Д  Е")
    print("  ╔══════════════════╗     ╔══════════════════╗")
    print(f"1 ║ {rival_grid[1, 1]}  {rival_grid[2, 1]}  {rival_grid[3, 1]}  {rival_grid[4, 1]}  {rival_grid[5, 1]}"
          f"  {rival_grid[6, 1]} ║   1 ║ {own_grid[1, 1]}  {own_grid[2, 1]}  {own_grid[3, 1]}  {own_grid[4, 1]}"
          f"  {own_grid[5, 1]}  {own_grid[6, 1]} ║")
    print(f"2 ║ {rival_grid[1, 2]}  {rival_grid[2, 2]}  {rival_grid[3, 2]}  {rival_grid[4, 2]}  {rival_grid[5, 2]}"
          f"  {rival_grid[6, 2]} ║   2 ║ {own_grid[1, 2]}  {own_grid[2, 2]}  {own_grid[3, 2]}  {own_grid[4, 2]}"
          f"  {own_grid[5, 2]}  {own_grid[6, 2]} ║")
    print(f"3 ║ {rival_grid[1, 3]}  {rival_grid[2, 3]}  {rival_grid[3, 3]}  {rival_grid[4, 3]}  {rival_grid[5, 3]}"
          f"  {rival_grid[6, 3]} ║   3 ║ {own_grid[1, 3]}  {own_grid[2, 3]}  {own_grid[3, 3]}  {own_grid[4, 3]}"
          f"  {own_grid[5, 3]}  {own_grid[6, 3]} ║")
    print(f"4 ║ {rival_grid[1, 4]}  {rival_grid[2, 4]}  {rival_grid[3, 4]}  {rival_grid[4, 4]}  {rival_grid[5, 4]}"
          f"  {rival_grid[6, 4]} ║   4 ║ {own_grid[1, 4]}  {own_grid[2, 4]}  {own_grid[3, 4]}  {own_grid[4, 4]}"
          f"  {own_grid[5, 4]}  {own_grid[6, 4]} ║")
    print(f"5 ║ {rival_grid[1, 5]}  {rival_grid[2, 5]}  {rival_grid[3, 5]}  {rival_grid[4, 5]}  {rival_grid[5, 5]}"
          f"  {rival_grid[6, 5]} ║   5 ║ {own_grid[1, 5]}  {own_grid[2, 5]}  {own_grid[3, 5]}  {own_grid[4, 5]}"
          f"  {own_grid[5, 5]}  {own_grid[6, 5]} ║")
    print(f"6 ║ {rival_grid[1, 6]}  {rival_grid[2, 6]}  {rival_grid[3, 6]}  {rival_grid[4, 6]}  {rival_grid[5, 6]}"
          f"  {rival_grid[6, 6]} ║   6 ║ {own_grid[1, 6]}  {own_grid[2, 6]}  {own_grid[3, 6]}  {own_grid[4, 6]}"
          f"  {own_grid[5, 6]}  {own_grid[6, 6]} ║")
    print("  ╚══════════════════╝     ╚══════════════════╝")
    print("\x1b[0;30;41m" + message + "\x1b[0m")
    print(low_line)