Feature: Users can be added/removed/edited

Scenario: Attempting to create user without email and/or password
	Given there exists no user with email "user01@mail.com" registered in the DB
	 When the /user endpoint receives a POST request with email "user01@mail.com" and no password
	 Then response status is Forbidden
	  And response message says: "Missing email and/or password. Both required."

	Given there exists no user with email "user01@mail.com" registered in the DB
	 When the /user endpoint receives a POST request without email
	 Then response status is Forbidden
	  And response message says: "Missing email and/or password. Both required."

Scenario: Attempting to create user that already exists
	Given a user with email "user01@mail.com" and password "mypass" is registered in the DB
	 When the /user endpoint receives a POST request with email "user01@mail.com" and password "mypass"
	 Then response status is Forbidden
	  And response message says: "User already exists."

Scenario: Creating a new user with default profile
	Given there exists no user with email "user01@mail.com" registered in the DB
	 When the /user endpoint receives a POST request with email "user01@mail.com" and password "mypass"
	 Then response contains a valid access token

Scenario: Editing user profile
	Given a user with email "user01@mail.com" and password "mypass" is registered in the DB
	  And we have a valid access token for user with email "user01@mail.com" and password "mypass"
	 When the /user endpoint receives a PATCH request with first_name "John", last_name "Doe", address "Big house", country "Atlantida", city "Atlantic City", language "en-US", role "user"
	 Then response status is OK

	Given we have a valid access token for user with email "user01@mail.com" and password "mypass"
	 When the /user endpoint receives a GET request
	 Then response contains email "user01@mail.com", first_name "John", last_name "Doe", address "Big house", country "Atlantida", city "Atlantic City", language "en-US", role "user"

@wip
Scenario: Deleting user profile