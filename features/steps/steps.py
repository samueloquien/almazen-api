from behave import *
from hamcrest import *
import json


@given('a user with email {email} and password {password} is registered in the DB')
def step_impl(context, email, password):
	context._.create_user(email, password)

@when('the {endpoint_name} endpoint receives a POST request with email {email} and password {password}')
def step_impl(context, endpoint_name, email, password):
	context._.call_api_post(endpoint_name, body={'email':email, 'password':password})

@then('response contains a valid access token')
def step_impl(context):
	r = context._.responses[-1]
	data = json.loads(r.data.decode())
	assert_that(data, has_key('access_token') , 'response contains an access token')


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


