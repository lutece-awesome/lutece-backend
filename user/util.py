from user.models import Solve


def update_user_solve(usr, prob, status):
    s, created = Solve.objects.get_or_create(user=usr, problem=prob)
    if not s.status and status is True:
        s.status = True
        s.save()
