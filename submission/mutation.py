import graphene
from annoying.functions import get_object_or_None
from django.conf import settings
from graphql_jwt.decorators import login_required

from data.service import DataService
from judge.models import JudgeResult as JudgeResultModel
from judge.result import JudgeResult
from judge.tasks import apply_submission
from problem.models import Problem
from submission.form import SubmitSubmissionForm
from submission.models import Submission, SubmissionAttachInfo


class SubmitSubmission(graphene.Mutation):
    class Arguments:
        problem_slug = graphene.String(required=True)
        code = graphene.String(required=True)
        language = graphene.String(required=True)

    pk = graphene.ID()

    @login_required
    def mutate(self, info, *args, **kwargs):
        form = SubmitSubmissionForm(kwargs)
        if form.is_valid():
            values = form.cleaned_data
            problem = get_object_or_None(Problem, slug=values['problem_slug'])
            attach_info = SubmissionAttachInfo(cases_count=DataService.get_cases_count(problem.pk))
            result = JudgeResultModel(_result=JudgeResult.PD.full)
            sub = Submission(
                code=values.get('code'),
                _language=values.get('language'),
                user=info.context.user,
                problem=problem
            )
            attach_info.save()
            result.save()
            sub.attach_info = attach_info
            sub.result = result
            sub.save()
            apply_submission.apply_async(args=(sub.get_judge_field(),), queue=settings.JUDGE.get('task_queue'))
            problem.ins_submit_times()
            return SubmitSubmission(pk=sub.pk)
        else:
            raise RuntimeError(form.errors.as_json())


class Mutation(graphene.AbstractType):
    submit_submission = SubmitSubmission.Field()
