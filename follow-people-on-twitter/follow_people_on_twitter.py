#!/usr/bin/python3

import sys
import csv
import twitter
import time
import random
import configparser

def parse_file(file_name):
    print(file_name)
    people = list()
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for line in reader:
            people.append(line)
    return people

def wait(config):
    wait_time = random.randint(int(config['INFO']['min_time']), int(config['INFO']['max_time']))
    #print("Choosing time between %d and %d - waiting %d seconds before next action" % (config['INFO']['min_time'], config['INFO']['max_time'], wait_time))
    time.sleep(wait_time)

def follow_people(api, people, config):
    #print(people)
    count_followed = 0
    total_people = len(people)
    print('Going to follow %d people (this is going to take between %d and %d seconds to complete)' % (total_people, int(config['INFO']['min_time']) * total_people, int(config['INFO']['max_time']) * total_people))
    for i in range(total_people):
        account_name = people[i]
        try:
            person = api.CreateFriendship(screen_name=people[i])
            print(account_name, 'has been followed')
            count_followed = count_followed + 1
        except twitter.error.TwitterError as e:
            print('error for ', account_name, e)
            pass
        #Just to be safe and avoid receiving 40X from twitter's API
        wait(config)
    print(count_followed, 'people out of ', total_people, 'have been followed')


def main():
    try:
        config = configparser.ConfigParser()
        config.read(['config.cfg', 'config.local.cfg'])
        api = twitter.Api(consumer_key=config['TWITTER']['consumer_key'],
                          consumer_secret=config['TWITTER']['consumer_secret'],
                          access_token_key=config['TWITTER']['access_token_key'],
                          access_token_secret=config['TWITTER']['access_token_secret'])
        if len(sys.argv) > 1:
            people = parse_file(sys.argv[1])
            follow_people(api, people, config)
        else:
            print('Please provide the filename')
    except Exception as e:
        print('error', e)

main()
