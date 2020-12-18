from settings import endpoint

@endpoint('/login')
def login_user():
    return {
        'name': "Sample",
    }
