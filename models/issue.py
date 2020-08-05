from odoo import models, fields, api


class Issue(models.Model):
    _name = 'issue.issue'
    _description = 'An issue that needs tracked (RMAs etc)'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]

    name = fields.Char()
    description = fields.Html(string='Description')
    user_ids = fields.One2many(
        'res.users',
        'id',
        string='Assigned To',
    )
    category_id = fields.Many2one(
        'issue.category',
        string='Category',
    )
    state = fields.Selection([
            ('needs action', 'Needs Action'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        string='Status',
        default='needs action',
    )
    last_checked = fields.Datetime('Last Checked')
    communication_ids = fields.Many2many(
        'issue.communication',
        'id',
        string='External Communications',
    )
    old_id = fields.Integer()


class IssueCategory(models.Model):
    _name = 'issue.category'
    _description = 'Different Categories for Issues'

    name = fields.Char()
    color_id = fields.Many2one(
        'issue.category.color',
        string='Color',
    )

    @api.onchange('color_id')
    @api.multi
    def _compute_name(self):
        self.name = f'{self.name.split("-")[0]} - {self.color_id.name}'


class IssueCategoryColor(models.Model):
    _name = 'issue.category.color'
    _description = 'Color code for Issue Categories'

    name = fields.Char(string='Color')


class IssueCommunication(models.Model):
    _name = 'issue.communication'
    _description = 'Different Places Communication about the issue happened'

    name = fields.Char(compute='_compute_name')
    channel_id = fields.Many2one(
        'issue.communication.channel',
        string='Channel',
        oldname='channel',
    )
    identifier = fields.Char(string='Identifier')

    @api.depends('channel_id', 'identifier')
    @api.multi
    def _compute_name(self):
        for communication in self:
            communication.name = f'{communication.channel_id.name}: {communication.identifier}'


class IssueCommunicationChannel(models.Model):
    _name = 'issue.communication.channel'
    _description = 'Platform or Record communication happened'

    name = fields.Char()
