from problem.models import Problem
from user.models import User, Solve


def update_user_solve(usr: User, prob: Problem, status: bool):
    solve, created = Solve.objects.get_or_create(user=usr, problem=prob)
    if not solve.status and status is True:
        solve.status = True
        solve.save()
