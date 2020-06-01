from behave import *
from hamcrest import *
import json


@given('a user with email "{email}" and password "{password}" is registered in the DB')
def step_impl(context, email, password):
	context._.create_user(email, password)

@given('there exists no user with email "{email}" registered in the DB')
def step_impl(context, email):
	assert_that(context._.user_exists(email), not_(True), 'no user exists with email {}'.format(email))

@when('the {endpoint_name} endpoint receives a POST request with email "{email}" and password "{password}"')
def step_impl(context, endpoint_name, email, password):
	context._.call_api_post(endpoint_name, body={'email':email, 'password':password})

@then('response contains a valid access token')
def step_impl(context):
	data = context._.get_response_data()
	assert_that(data, has_key('access_token') , 'response contains an access token')

@then('response status is {status}')
def step_impl(context, status):
	r = context._.responses[-1]
	response_status = r.status # 200 OK
	response_status_str = response_status.split(' ')[1]
	expected_status = status.upper()
	assert_that(response_status_str, equal_to(expected_status), 'response status is {}'.format(status))

@then('response message says: "{expected_message}"')
def step_impl(context, expected_message):
	r = context._.responses[-1]
	response_message = context._.get_response_data()['message']
	assert_that(response_message, equal_to(expected_message), 'response message is {}'.format(expected_message))


@given(u'a user is created with email {email} and password {passwd}')
def step_impl(context, email, passwd):
	print('About to create user {}/{}'.format(email,passwd))
	context.users = [email]


@when(u'the user/profile endpoint receives a POST request with field xxx set to yyy')
def step_impl(context):
	pass


@when(u'the user/profile endpoint receives a GET request')
def step_impl(context):
	pass

@then(u'response contains field {field} with value {value}')
def step_impl(context, field, value):
	assert_that(context.users[0], equal_to(value), 'Expected value')


@given(u'a user is created with profile fields specified')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given a user is created with profile fields specified')


@then(u'response contains the provided values for fields first_name, last_name, country, etc')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then response contains the provided values for fields first_name, last_name, country, etc')


