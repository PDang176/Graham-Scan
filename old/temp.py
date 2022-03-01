from display import run
from graham_scan import create_points

def main():
    prompt = "How many nodes would you like to spawn? "
    n = int(input(prompt))
    create_points(n)
    run()

if __name__ == "__main__":
    main()