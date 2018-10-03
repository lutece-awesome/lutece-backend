import graphene


class SubmitSubmission(graphene.Mutation):

    class Arguments:
        problemslug = graphene.String( required = True )
        code = graphene.String( required = True )
        language = graphene.String( required = True )

    pk = graphene.ID()

    @login_required
    def mutate(self, info, ** kwargs):
        from submission.form import SubmitSubmissionForm
        from data_server.util import get_case_number
        from submission.judge_result import Judge_result
        from problem.util import InsSubmittimes
        from Lutece.settings import TASK_QUEUE
        SolutionForm = SubmitSolutionForm(kwargs)
        if SolutionForm.is_valid():
            values = SolutionForm.cleaned_data
            problem = get_object_or_None(Problem, slug=values['problemslug'])
            s = Submission(
                language=values['language'],
                user=info.context.user,
                problem=problem,
                case_number=get_case_number(problem.pk),
                judge_status=Judge_result.PD.value.full,
                code=values['code'])
            s.save()
            Submission_task.apply_async(
                args=(s.get_push_dict(),), queue=TASK_QUEUE)
            InsSubmittimes(problem.pk)
            return SubmitSolution(pk=s.pk)
        else:
            raise RuntimeError(SolutionForm.errors.as_json())