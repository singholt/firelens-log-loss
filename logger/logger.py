import time
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Log generator with configurable rates')
    parser.add_argument('steady_rate', type=int, help='The steady rate of log generation')
    parser.add_argument('burst', type=int, help='The burst amount')
    parser.add_argument('time_in_minutes', type=int, help='Duration in minutes')
    parser.add_argument('output_file', type=str, nargs='?', help='Optional file path to write logs')
    return parser.parse_args()


def write_event(message, output_file=None):
    if output_file:
        with open(output_file, 'a') as f:
            f.write(message + '\n')
            f.flush()
    else:
        print(message, flush=True)


def print_event(i, output_file=None):
    message = "Message: " + str(i)
    write_event(message, output_file)


def main():
    args = parse_args()

    time_in_seconds = 60 * args.time_in_minutes

    # Create or clear the output file if specified
    if args.output_file:
        # Create/clear the file
        with open(args.output_file, 'w') as f:
            pass  # Just create/clear the file

    start = time.time()
    for i in range(1, time_in_seconds * args.steady_rate):
        print_event(i, args.output_file)
        if i % args.steady_rate == 0:
            to_wait = 1 - time.time() + start
            if to_wait > 0:
                time.sleep(to_wait)
            start = time.time()

    so_far = time_in_seconds * args.steady_rate

    for i in range(so_far, so_far + args.burst + 1):
        print_event(i, args.output_file)


if __name__ == '__main__':
    main()
