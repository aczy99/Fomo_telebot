# Creating string for event
import telebot




def event_string(event):
    header = "Event " + str(event.id)
    title = "      Title: " + event.title
    date = "      Date time: " + str(event.date)
    description = "      Description: " + event.description
    venue = "      Venue: " + event.venue
    category = "      Category: " + event.category
    overall = header + "\n" + title + "\n" + date + "\n" + description + "\n" + category + "\n" + venue + "\n"
    return overall


