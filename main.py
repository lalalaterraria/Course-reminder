
import bin.Reminder as rd

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()

    Main = rd._Main()
    Main.main()