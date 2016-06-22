USERS = {'admin':'50300118',
          'root':'123'}
GROUPS = {'admin':['group:editors'], 'root':['group:editors']}

def groupfinder(userid, request):
    if userid in USERS:
        print(GROUPS.get(userid))
        return GROUPS.get(userid)
