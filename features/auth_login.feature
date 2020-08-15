
Feature: user_login


Scenario: Login to an existing user
	Given a user with email "user01@mail.com" and password "mypass" is registered in the DB
	 When the /auth/login endpoint receives a POST request with email "user01@mail.com" and password "mypass"
	 Then response contains a valid access token

Scenario: Login to a non existing user
	Given there exists no user with email "user01@mail.com" registered in the DB
	 When the /auth/login endpoint receives a POST request with email "user01@mail.com" and password "any_pass"
	 Then response status is Unauthorized
	  And response message says: "Email doesn't exist."

Scenario: Login with invalid password
	Given a user with email "user01@mail.com" and password "mypass" is registered in the DB
	 When the /auth/login endpoint receives a POST request with email "user01@mail.com" and password "another_pass"
	 Then response status is Unauthorized
	  And response message says: "Invalid email/password."