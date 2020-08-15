from behave import given, when, then, step
from hamcrest import assert_that, equal_to, has_key, not_
import hamcrest
import json
from pydoc import locate
import re


@given('a user with email "{email}" and password "{password}" is registered in the DB')
def step_impl(context, email, password):
	context._.create_user(email, password)

@given('we have a valid access token for user with email "{email}" and password "{password}"')
def step_impl(context, email, password):
	context._.call_api_post('/auth/login', body={'email':email, 'password':password})
	data = context._.get_response_data()
	assert_that(data, has_key('access_token'))
	context._.access_token = data['access_token']

@given('there exists no user with email "{email}" registered in the DB')
def step_impl(context, email):
	assert_that(context._.user_exists(email), not_(True), 'no user exists with email {}'.format(email))

@when('the {endpoint_name} endpoint receives a POST request with email "{email}" and password "{password}"')
def step_impl(context, endpoint_name, email, password):
	context._.call_api_post(endpoint_name, body={'email':email, 'password':password})

@when('the {endpoint_name} endpoint receives a POST request with email "{email}" and no password')
def step_impl(context, endpoint_name, email):
	context._.call_api_post(endpoint_name, body={'email':email})

@when('the {endpoint_name} endpoint receives a POST request without email')
def step_impl(context, endpoint_name):
	context._.call_api_post(endpoint_name)

@when('the {endpoint_name} endpoint receives a PATCH request with first_name "{first_name}", last_name "{last_name}", address "{address}", country "{country}", city "{city}", language "{language}", role "{role}"')
def step_impl(context, endpoint_name, first_name, last_name, address, country, city, language, role):
	data = {
		'first_name': first_name, 'last_name': last_name, 'address': address,
		'country': country, 'city': city, 'language': language, 'role': role
	}
	context._.call_api_patch(endpoint_name, body=data)


@when('the {endpoint_name} endpoint receives a GET request')
def step_impl(context, endpoint_name):
	context._.call_api_get(endpoint_name)

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
	one = '1'
	two = '2'
	assert_that(one, equal_to(two), 'impossible is nothing')

@then('response contains email "{email}", first_name "{first_name}", last_name "{last_name}", address "{address}", country "{country}", city "{city}", language "{language}", role "{role}"')
def step_impl(context, email, first_name, last_name, address, country, city, language, role):
	print('Debugging here')
	data = context._.get_response_data()['user_profile']
	print(data)
	one = '1'
	two = '2'
	print('one:',one,'   two:',two)
	assert_that(one, equal_to(two), 'impossible is nothing')
	print('flag1')
	#assert_that(one, equal_to(two))#, 'aritmetic order')
	actual = data['email']
	expected = email
	assert_that(actual, equal_to(expected), 'response message is {}'.format(expected))
	#assert_that(data.keys(), has_items('email,first_name'.split(',')), 'email is expected')
	print('flag11')
	assert_that(data['email'], equal_to(email), 'email is expected')
	print('flag2')
	print(data['first_name'])
	print(first_name)
	print('hi')
	assert_that(data['first_name'], equal_to(first_name), 'first_name is expected')
	print('flag3')
	assert_that(data['last_name'], equal_to(last_name), 'last_name is expected')
	print('flag4')
	assert_that(data['address'], equal_to(address), 'address is expected')
	print('flag5')
	assert_that(data['country'], equal_to(country), 'country is expected')
	print('flag6')
	assert_that(data['city'], equal_to(city), 'city is expected')
	assert_that(data['language'], equal_to(language), 'language is expected')
	assert_that(data['role'], equal_to(role), 'role is expected')

@given(u'a user is created with email {email} and password {passwd}')
def step_impl(context, email, passwd):
	print('About to create user {}/{}'.format(email,passwd))
	context.users = [email]


@when(u'the user/profile endpoint receives a POST request with field xxx set to yyy')
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


