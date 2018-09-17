const JudgeResult = {
	PD: 0,
	PR: 1,
	AC: 2,
	RN: 3,
	CE: 4,
	WA: 5,
	RE: 6,
	TLE: 7,
	OLE: 8,
	MLE: 9,
	JE: 10,

	valueOf: {
		Pending: 0,
		Preparing: 1,
		Accepted: 2,
		Running: 3,
		'Compile Error': 4,
		'Wrong Answer': 5,
		'Runtime Error': 6,
		'Time Limit Exceeded': 7,
		'Output Limit Exceeded': 8,
		'Memory Limit Exceeded': 9,
		'Judger Error': 10,
	},
};

const JudgeResultUtil = {
	JudgeResult(result) {
		return JudgeResult.valueOf(result);
	},

};


export default JudgeResultUtil;
