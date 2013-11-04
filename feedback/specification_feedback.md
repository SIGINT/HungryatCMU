Project Specifcation Feedback
============

I see a ERD, but that's definitely not the same thing as wireframes, which should be mockups or sketches of what each page in the application looks like. For the models, there are some relational aspects which should be considered. For example, it might make more sense for an order to have a manytomany relation to food items. A student creates an order with multiple food items on it, such as a burger, an order of fries, and a coke. Also, if there's administrator control, then a model for the administrator user should be made. For the actions, some details should be considered such as how exactly filtering works for student searches: does a location filter go through building_name? location_desciption? all of the attributes in the location model? There's also one action that seems to be missing: how are restaurants added in the first place? By administrators? Also, are restaurant employees assigned to restaurants when the administrator sends the registration link? The backlog for Sprint 1 seems reasonable, just be careful about the various access control rules (such as student vs employee vs administrator). Also, make sure to designate a person to be the product owner for Sprint 1. 

---

Feedback by: Jason Tsay (jtsay@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team60/blob/master/feedback/specification_feedback.md
