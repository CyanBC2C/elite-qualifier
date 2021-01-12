"""
Author: Cyan Brown
Project: C2C Webscraping / Analysis
Date: 1/3/2021

Info:
  I cannot get the number of votes when the poll hasn't finished - that is why in some cases there is a link instead.

Instructions:
  This project enables the user to quickly search polls, their answers, and even graphs them.

  Type in the keywords of a poll that you want to find. After type the number that denotes the question.
"""

# reddit api library
import praw

# formatting library
from rich import print as pprint
from rich.console import Console
from rich.table import Table

import matplotlib.pyplot as plt


console = Console()


# setting up reddit access through OAUTH
SECRET = '8RSEcfUn7fuxPhDg4F3g0ZilysAJ3Q'
CLIENT_ID = '-93MMkyMTCQ4Hg'

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET,
                     password="CBrown29",
                     user_agent="Meme Analyzer by /u/CyanBrownC2C",
                     username="CyanBrownC2C")

# Poll subreddit name
subreddit = "Polls"

print("[+] Gathering polls...")

# Getting the posts
subreddit = reddit.subreddit(subreddit)
posts = subreddit.hot(limit=1000)

# Setting data that will ease search
posts_dict = {i:k for i,k in enumerate(posts)}
posts_title = [i.title for i in posts_dict.values()]

def main():
  # global variables
  global posts_dict
  global posts_title
  global table

  # getting and parsing input keywords
  search_words = input("Enter keywords (seperate with ','): ")
  search_words = search_words.lower().replace(', ',',').split(",")

  print("[+] Searching for relevant polls...")

  # finding posts based on search words
  use_polls = []
  for i in search_words:
    for k in posts_title:
      if i in k.lower():
        use_polls.append(posts_dict[posts_title.index(k)])

  tab = Table(show_header=True,header_style='bold cyan',show_lines=True)
  tab.add_column("ID",justify="left")
  tab.add_column("Question",justify="left")

  # Creating table of found posts
  posts_dict2 = {i:k for i,k in enumerate(use_polls)}
  for i in posts_dict2.keys():
    tab.add_row(str(i),posts_dict2[i].title)

  console.print(tab)

  post_num = input("Which poll do you want to inspect? (use id number) ('exit' to search): ")
  print()

  # Allowing people to exit before further searching
  if post_num=='exit':
    del posts_dict2
    del use_polls
    main()

  # Getting the final post they want to view
  post = posts_dict2[int(post_num)]
  poll_data = post.poll_data

  print(f"There are {poll_data.total_vote_count} votes total.")
  print()

  table = Table(show_header=True, header_style="bold magenta",show_lines=True)

  table.add_column(post.title,justify="left")
  table.add_column("Votes",justify="left")

  ans = []
  votes = []

  # Looping through answer choices
  for option in poll_data.options:
    try:
      table.add_row(
        str(option.text), 
        str(option.vote_count)
      )

      ans.append(option.text)
      votes.append(option.vote_count)
      
    except AttributeError:

      # If poll doesn't have a count available, it uses link
      if poll_data.options.index(option) == 0:
        url = "/".join(post.url.split("/")[:-2])
        pprint(f"[red][*] Poll count could not be found, use link: {url}[/red]")
        print()

      table.add_row(
        str(option.text),
        "N/A"
      )

  console.print(table)
  print()

  if ans != []:
    plt.bar(ans, votes)
    plt.title('Question and Votes')
    plt.xlabel('Question')
    plt.ylabel('Votes')
    plt.show()

  pprint("[red][*] 'exit' to search, 'quit' to quit:[/red]")

  # final input of person
  info = input()
  if info == 'exit':
    main()
  elif info == 'quit':
    quit(0)

main()