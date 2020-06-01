
@wip
Feature: user_login


Scenario: Logging to an existing user
	Given a user with email user01@mail.com and password mypass is registered in the DB
	When the /auth/login endpoint receives a POST request with email user01@mail.com and password mypass
	Then response contains a valid access token

