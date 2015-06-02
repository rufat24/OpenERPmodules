from openerp.osv import osv, fields
from openerp import netsvc

class plan_carry(osv.osv):
    _name= 'plan.carry'
    _columns= {
        'type': fields.selection([('vote','Voting'),('poll','Poll')],'Type'),
        'group': fields.char('User Group'),
        'start_date': fields.date('Start Date'),
        'finish_date': fields.date('Finish Date'),
        'state': fields.selection([('new','New'),('done','Done')]),
    }
class voting_tasks(osv.osv):
    _name='voting.tasks'
    _columns={
        'name': fields.char('The Name of the Vote'),
        'group': fields.char('User Group'),
        'start_date': fields.date('Start Date'),
        'finish_date': fields.date('Finish Date'),
        'responsible': fields.many2one('res.users','Responsible'),
        'state': fields.selection([('new1','New'),('confirm1','Confirm'),('done1','Done')]),
        'answer_line': fields.one2many('voiting.answers','partner_id'),
        'answer_id': fields.related('answer_line','answer_id',type="many2one",relation="answer.type")
        }
class voiting_answers(osv.osv):
    _name='voiting.answers'
    _columns={
        'partner_id': fields.integer('Partner ID'),
        'answer_id': fields.many2one('answer.type','Variant of Answers'),
        }
class answer_type(osv.osv):
    _name='answer.type'
    _columns={
        'answer_name': fields.char('Variants of Answers',required=True)
        }

class question_tasks(osv.osv):
    _name='question.tasks'
    _columns={
        'name': fields.char('The Name of the Surveys'),
        'group': fields.char('User Group'),
        'start_date': fields.date('Start Date'),
        'finish_date': fields.date('Finish Date'),
        'responsible': fields.many2one('res.users','Responsible'),
        'state': fields.selection([('new2','New'),('confirm2','Confirm'),('done2','Done')]),
        'question_line': fields.one2many('voiting.questions','partner_id'),
        'question_id': fields.related('question_line','question_id',type="many2one",relation="question.type")
    }
class voting_question(osv.osv):
    _name='voiting.questions'
    _columns={
        'question_id': fields.many2one('question.type','A List of Questions'),
        'partner_id': fields.integer('Partner ID')
        }

class question_type(osv.osv):
    _name='question.type'
    _columns={
        'question_name': fields.char('Variants of Questions',required=True)
        }