
Feature: user_profile


Scenario: Registering a new user
Given a user is created with profile fields specified
When the user/profile endpoint receives a GET request
Then response contains the provided values for fields first_name, last_name, country, etc

Scenario: Editing user profile
Given a user is created with email john@mail.com and password mysecret
When the user/profile endpoint receives a POST request with field xxx set to yyy
And the user/profile endpoint receives a GET request
Then response contains field email with value john@mail.com
