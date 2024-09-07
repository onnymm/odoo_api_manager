from typing import Literal

MOST_COMMON_FIELDS = Literal[
    'access_token',
    'access_url',
    'access_warning',
    'account_id',
    'active',
    'activity_calendar_event_id',
    'activity_date_deadline',
    'activity_exception_decoration',
    'activity_exception_icon',
    'activity_ids',
    'activity_state',
    'activity_summary',
    'activity_type_icon',
    'activity_type_id',
    'activity_user_id',
    'amount',
    'attachment_ids',
    'body',
    'can_publish',
    'category_id',
    'child_ids',
    'code',
    'color',
    'company_currency_id',
    'company_id',
    'country_code',
    'country_id',
    'create_date',
    'create_uid',
    'currency_id',
    'date',
    'date_deadline',
    'date_from',
    'department_id',
    'description',
    'display_name',
    'email',
    'employee_id',
    'has_message',
    'id',
    'image_1024',
    'image_128',
    'image_1920',
    'image_256',
    'image_512',
    'is_published',
    'journal_id',
    'key',
    'lang',
    'line_ids',
    'location_id',
    'message',
    'message_attachment_count',
    'message_follower_ids',
    'message_has_error',
    'message_has_error_counter',
    'message_has_sms_error',
    'message_ids',
    'message_is_follower',
    'message_needaction',
    'message_needaction_counter',
    'message_partner_ids',
    'model',
    'model_id',
    'move_ids',
    'my_activity_date_deadline',
    'name',
    'note',
    'parent_id',
    'parent_path',
    'partner_id',
    'partner_ids',
    'priority',
    'product_id',
    'product_tmpl_id',
    'product_uom_category_id',
    'product_uom_id',
    'project_id',
    'quant_ids',
    'quantity',
    'rating_ids',
    'reference',
    'res_id',
    'res_model',
    'resource_calendar_id',
    'sale_order_count',
    'sequence',
    'state',
    'subject',
    'tag_ids',
    'team_id',
    'template_id',
    'type',
    'tz',
    'url',
    'user_id',
    'user_ids',
    'value',
    'warehouse_id',
    'website_id',
    'website_message_ids',
    'website_published',
    'website_url',
    'write_date',
    'write_uid',
    'xml_id'
]

MODELS = Literal[
    'account.account',
    'account.account.tag',
    'account.accrued.orders.wizard',
    'account.aged.partner.balance.report.handler',
    'account.aged.payable.report.handler',
    'account.aged.receivable.report.handler',
    'account.analytic.account',
    'account.analytic.applicability',
    'account.analytic.distribution.model',
    'account.analytic.line',
    'account.analytic.plan',
    'account.asset',
    'account.asset.report.handler',
    'account.auto.reconcile.wizard',
    'account.automatic.entry.wizard',
    'account.bank.selection',
    'account.bank.statement',
    'account.bank.statement.line',
    'account.bank.statement.line.transient',
    'account.cash.flow.report.handler',
    'account.cash.rounding',
    'account.change.lock.date',
    'account.chart.template',
    'account.deferred.expense.report.handler',
    'account.deferred.report.handler',
    'account.deferred.revenue.report.handler',
    'account.disallowed.expenses.category',
    'account.disallowed.expenses.rate',
    'account.disallowed.expenses.report.handler',
    'account.ec.sales.report.handler',
    'account.edi.common',
    'account.edi.xml.cii',
    'account.edi.xml.ubl_20',
    'account.edi.xml.ubl_21',
    'account.edi.xml.ubl_a_nz',
    'account.edi.xml.ubl_bis3',
    'account.edi.xml.ubl_de',
    'account.edi.xml.ubl_efff',
    'account.edi.xml.ubl_nl',
    'account.edi.xml.ubl_sg',
    'account.financial.year.op',
    'account.fiscal.position',
    'account.fiscal.position.account',
    'account.fiscal.position.tax',
    'account.fiscal.year',
    'account.followup.report',
    'account.full.reconcile',
    'account.general.ledger.report.handler',
    'account.generic.tax.report.handler',
    'account.generic.tax.report.handler.account.tax',
    'account.generic.tax.report.handler.tax.account',
    'account.group',
    'account.incoterms',
    'account.invoice.report',
    'account.invoice_extract.words',
    'account.journal',
    'account.journal.group',
    'account.journal.report.handler',
    'account.missing.transaction.wizard',
    'account.move',
    'account.move.line',
    'account.move.reversal',
    'account.move.send',
    'account.multicurrency.revaluation.report.handler',
    'account.multicurrency.revaluation.wizard',
    'account.online.account',
    'account.online.link',
    'account.partial.reconcile',
    'account.partner.ledger.report.handler',
    'account.payment',
    'account.payment.method',
    'account.payment.method.line',
    'account.payment.register',
    'account.payment.term',
    'account.payment.term.line',
    'account.reconcile.model',
    'account.reconcile.model.line',
    'account.reconcile.model.partner.mapping',
    'account.reconcile.wizard',
    'account.report',
    'account.report.column',
    'account.report.custom.handler',
    'account.report.expression',
    'account.report.external.value',
    'account.report.file.download.error.wizard',
    'account.report.footnote',
    'account.report.horizontal.group',
    'account.report.horizontal.group.rule',
    'account.report.line',
    'account.resequence.wizard',
    'account.root',
    'account.setup.bank.manual.config',
    'account.tax',
    'account.tax.group',
    'account.tax.repartition.line',
    'account.tax.report.handler',
    'account.tax.unit',
    'account.tour.upload.bill',
    'account.tour.upload.bill.email.confirm',
    'account.transfer.model',
    'account.transfer.model.line',
    'account.trial.balance.report.handler',
    'account.unreconcile',
    'account_followup.followup.line',
    'account_followup.manual_reminder',
    'account_followup.missing.information.wizard',
    'account_reports.export.wizard',
    'account_reports.export.wizard.format',
    'analytic.mixin',
    'appointment.answer',
    'appointment.answer.input',
    'appointment.booking.line',
    'appointment.invite',
    'appointment.manage.leaves',
    'appointment.onboarding.link',
    'appointment.question',
    'appointment.resource',
    'appointment.slot',
    'appointment.type',
    'asset.modify',
    'auth_totp.device',
    'auth_totp.wizard',
    'avatar.mixin',
    'bank.rec.widget',
    'bank.rec.widget.line',
    'barcode.nomenclature',
    'barcode.rule',
    'barcodes.barcode_events_mixin',
    'base',
    'base.document.layout',
    'base.enable.profiling.wizard',
    'base.import.module',
    'base.language.export',
    'base.language.import',
    'base.language.install',
    'base.module.install.request',
    'base.module.install.review',
    'base.module.uninstall',
    'base.module.update',
    'base.module.upgrade',
    'base.partner.merge.automatic.wizard',
    'base.partner.merge.line',
    'base_import.import',
    'base_import.mapping',
    'bus.bus',
    'bus.presence',
    'calendar.alarm',
    'calendar.alarm_manager',
    'calendar.attendee',
    'calendar.booking',
    'calendar.booking.line',
    'calendar.event',
    'calendar.event.type',
    'calendar.filters',
    'calendar.popover.delete.wizard',
    'calendar.provider.config',
    'calendar.recurrence',
    'change.password.own',
    'change.password.user',
    'change.password.wizard',
    'confirm.stock.sms',
    'crm.activity.report',
    'crm.iap.lead.helpers',
    'crm.iap.lead.industry',
    'crm.iap.lead.mining.request',
    'crm.iap.lead.role',
    'crm.iap.lead.seniority',
    'crm.lead',
    'crm.lead.lost',
    'crm.lead.pls.update',
    'crm.lead.scoring.frequency',
    'crm.lead.scoring.frequency.field',
    'crm.lead2opportunity.partner',
    'crm.lead2opportunity.partner.mass',
    'crm.lost.reason',
    'crm.merge.opportunity',
    'crm.quotation.partner',
    'crm.recurring.plan',
    'crm.stage',
    'crm.tag',
    'crm.team',
    'crm.team.member',
    'decimal.precision',
    'digest.digest',
    'digest.tip',
    'discuss.channel',
    'discuss.channel.member',
    'discuss.channel.rtc.session',
    'discuss.gif.favorite',
    'discuss.voice.metadata',
    'documents.account.folder.setting',
    'documents.document',
    'documents.facet',
    'documents.folder',
    'documents.link_to_record_wizard',
    'documents.mixin',
    'documents.request_wizard',
    'documents.share',
    'documents.shared.spreadsheet',
    'documents.tag',
    'documents.workflow.action',
    'documents.workflow.rule',
    'extract.mixin',
    'fetchmail.server',
    'format.address.mixin',
    'gamification.badge',
    'gamification.badge.user',
    'gamification.badge.user.wizard',
    'gamification.challenge',
    'gamification.challenge.line',
    'gamification.goal',
    'gamification.goal.definition',
    'gamification.goal.wizard',
    'gamification.karma.rank',
    'gamification.karma.tracking',
    'google.gmail.mixin',
    'hr.contract.type',
    'hr.department',
    'hr.departure.reason',
    'hr.departure.wizard',
    'hr.employee',
    'hr.employee.base',
    'hr.employee.category',
    'hr.employee.cv.wizard',
    'hr.employee.public',
    'hr.employee.skill',
    'hr.employee.skill.log',
    'hr.employee.skill.report',
    'hr.holidays.cancel.leave',
    'hr.holidays.summary.employee',
    'hr.job',
    'hr.leave',
    'hr.leave.accrual.level',
    'hr.leave.accrual.plan',
    'hr.leave.allocation',
    'hr.leave.employee.type.report',
    'hr.leave.mandatory.day',
    'hr.leave.report',
    'hr.leave.report.calendar',
    'hr.leave.type',
    'hr.resume.line',
    'hr.resume.line.type',
    'hr.skill',
    'hr.skill.level',
    'hr.skill.type',
    'hr.work.location',
    'html.field.history.mixin',
    'iap.account',
    'iap.account.info',
    'iap.autocomplete.api',
    'iap.enrich.api',
    'image.mixin',
    'ir.actions.act_url',
    'ir.actions.act_window',
    'ir.actions.act_window.view',
    'ir.actions.act_window_close',
    'ir.actions.actions',
    'ir.actions.client',
    'ir.actions.report',
    'ir.actions.server',
    'ir.actions.todo',
    'ir.asset',
    'ir.attachment',
    'ir.autovacuum',
    'ir.binary',
    'ir.config_parameter',
    'ir.cron',
    'ir.cron.trigger',
    'ir.default',
    'ir.demo',
    'ir.demo_failure',
    'ir.demo_failure.wizard',
    'ir.exports',
    'ir.exports.line',
    'ir.fields.converter',
    'ir.filters',
    'ir.http',
    'ir.logging',
    'ir.mail_server',
    'ir.min.cron.mixin',
    'ir.model',
    'ir.model.access',
    'ir.model.constraint',
    'ir.model.data',
    'ir.model.fields',
    'ir.model.fields.selection',
    'ir.model.inherit',
    'ir.model.relation',
    'ir.module.category',
    'ir.module.module',
    'ir.module.module.dependency',
    'ir.module.module.exclusion',
    'ir.profile',
    'ir.property',
    'ir.qweb',
    'ir.qweb.field',
    'ir.qweb.field.barcode',
    'ir.qweb.field.contact',
    'ir.qweb.field.date',
    'ir.qweb.field.datetime',
    'ir.qweb.field.duration',
    'ir.qweb.field.float',
    'ir.qweb.field.float_time',
    'ir.qweb.field.html',
    'ir.qweb.field.image',
    'ir.qweb.field.image_url',
    'ir.qweb.field.integer',
    'ir.qweb.field.many2many',
    'ir.qweb.field.many2one',
    'ir.qweb.field.monetary',
    'ir.qweb.field.qweb',
    'ir.qweb.field.relative',
    'ir.qweb.field.selection',
    'ir.qweb.field.text',
    'ir.qweb.field.time',
    'ir.rule',
    'ir.sequence',
    'ir.sequence.date_range',
    'ir.ui.menu',
    'ir.ui.view',
    'ir.ui.view.custom',
    'ir.websocket',
    'ir_actions_account_report_download',
    'knowledge.article',
    'knowledge.article.favorite',
    'knowledge.article.member',
    'knowledge.article.stage',
    'knowledge.article.template.category',
    'knowledge.article.thread',
    'knowledge.cover',
    'knowledge.invite',
    'l10n_mx.report.handler',
    'l10n_mx_edi.certificate',
    'l10n_mx_edi.document',
    'l10n_mx_edi.global_invoice.create',
    'l10n_mx_edi.invoice.cancel',
    'l10n_mx_edi.payment.method',
    'l10n_mx_xml_polizas.xml_polizas_wizard',
    'lot.label.layout',
    'mail.activity',
    'mail.activity.mixin',
    'mail.activity.plan',
    'mail.activity.plan.template',
    'mail.activity.schedule',
    'mail.activity.todo.create',
    'mail.activity.type',
    'mail.alias',
    'mail.alias.domain',
    'mail.alias.mixin',
    'mail.alias.mixin.optional',
    'mail.blacklist',
    'mail.blacklist.remove',
    'mail.bot',
    'mail.compose.message',
    'mail.composer.mixin',
    'mail.followers',
    'mail.gateway.allowed',
    'mail.guest',
    'mail.ice.server',
    'mail.link.preview',
    'mail.mail',
    'mail.message',
    'mail.message.reaction',
    'mail.message.schedule',
    'mail.message.subtype',
    'mail.message.translation',
    'mail.notification',
    'mail.notification.web.push',
    'mail.partner.device',
    'mail.render.mixin',
    'mail.resend.message',
    'mail.resend.partner',
    'mail.shortcode',
    'mail.template',
    'mail.template.preview',
    'mail.template.reset',
    'mail.thread',
    'mail.thread.blacklist',
    'mail.thread.cc',
    'mail.thread.main.attachment',
    'mail.thread.phone',
    'mail.tracking.duration.mixin',
    'mail.tracking.value',
    'mail.wizard.invite',
    'onboarding.onboarding',
    'onboarding.onboarding.step',
    'onboarding.progress',
    'onboarding.progress.step',
    'payment.capture.wizard',
    'payment.link.wizard',
    'payment.method',
    'payment.provider',
    'payment.provider.onboarding.wizard',
    'payment.refund.wizard',
    'payment.token',
    'payment.transaction',
    'phone.blacklist',
    'phone.blacklist.remove',
    'picking.label.type',
    'planning.analysis.report',
    'planning.planning',
    'planning.recurrency',
    'planning.role',
    'planning.send',
    'planning.slot',
    'planning.slot.template',
    'portal.mixin',
    'portal.share',
    'portal.wizard',
    'portal.wizard.user',
    'pos.bill',
    'pos.category',
    'pos.close.session.wizard',
    'pos.combo',
    'pos.combo.line',
    'pos.config',
    'pos.daily.sales.reports.wizard',
    'pos.details.wizard',
    'pos.make.payment',
    'pos.order',
    'pos.order.line',
    'pos.pack.operation.lot',
    'pos.payment',
    'pos.payment.method',
    'pos.printer',
    'pos.session',
    'pos_preparation_display.display',
    'pos_preparation_display.order',
    'pos_preparation_display.order.stage',
    'pos_preparation_display.orderline',
    'pos_preparation_display.reset.wizard',
    'pos_preparation_display.stage',
    'privacy.log',
    'privacy.lookup.wizard',
    'privacy.lookup.wizard.line',
    'procurement.group',
    'product.attribute',
    'product.attribute.custom.value',
    'product.attribute.value',
    'product.catalog.mixin',
    'product.category',
    'product.document',
    'product.label.layout',
    'product.margin',
    'product.packaging',
    'product.pricelist',
    'product.pricelist.item',
    'product.product',
    'product.removal',
    'product.replenish',
    'product.supplierinfo',
    'product.tag',
    'product.template',
    'product.template.attribute.exclusion',
    'product.template.attribute.line',
    'product.template.attribute.value',
    'product.unspsc.code',
    'project.collaborator',
    'project.milestone',
    'project.project',
    'project.project.stage',
    'project.project.stage.delete.wizard',
    'project.share.wizard',
    'project.tags',
    'project.task',
    'project.task.burndown.chart.report',
    'project.task.recurrence',
    'project.task.stage.personal',
    'project.task.type',
    'project.task.type.delete.wizard',
    'project.update',
    'publisher_warranty.contract',
    'purchase.bill.union',
    'purchase.order',
    'purchase.order.line',
    'purchase.report',
    'rating.mixin',
    'rating.parent.mixin',
    'rating.rating',
    'report.account.report_hash_integrity',
    'report.account.report_invoice',
    'report.account.report_invoice_with_payments',
    'report.base.report_irmodulereference',
    'report.hr_holidays.report_holidayssummary',
    'report.hr_skills.report_employee_cv',
    'report.layout',
    'report.paperformat',
    'report.point_of_sale.report_invoice',
    'report.point_of_sale.report_saledetails',
    'report.pos.order',
    'report.product.report_pricelist',
    'report.product.report_producttemplatelabel2x7',
    'report.product.report_producttemplatelabel4x12',
    'report.product.report_producttemplatelabel4x12noprice',
    'report.product.report_producttemplatelabel4x7',
    'report.product.report_producttemplatelabel_dymo',
    'report.project.task.user',
    'report.sign.green_savings_report',
    'report.stock.label_product_product_view',
    'report.stock.quantity',
    'report.stock.report_reception',
    'report.stock.report_stock_rule',
    'res.bank',
    'res.company',
    'res.config',
    'res.config.installer',
    'res.config.settings',
    'res.country',
    'res.country.group',
    'res.country.state',
    'res.currency',
    'res.currency.rate',
    'res.groups',
    'res.lang',
    'res.partner',
    'res.partner.autocomplete.sync',
    'res.partner.bank',
    'res.partner.category',
    'res.partner.industry',
    'res.partner.title',
    'res.users',
    'res.users.apikeys',
    'res.users.apikeys.description',
    'res.users.apikeys.show',
    'res.users.deletion',
    'res.users.identitycheck',
    'res.users.log',
    'res.users.settings',
    'res.users.settings.volumes',
    'reset.view.arch.wizard',
    'resource.calendar',
    'resource.calendar.attendance',
    'resource.calendar.leaves',
    'resource.mixin',
    'resource.resource',
    'sale.advance.payment.inv',
    'sale.mass.cancel.orders',
    'sale.order',
    'sale.order.cancel',
    'sale.order.discount',
    'sale.order.line',
    'sale.order.option',
    'sale.order.template',
    'sale.order.template.line',
    'sale.order.template.option',
    'sale.payment.provider.onboarding.wizard',
    'sale.report',
    'save.spreadsheet.template',
    'sequence.mixin',
    'sign.duplicate.template.pdf',
    'sign.item',
    'sign.item.option',
    'sign.item.role',
    'sign.item.type',
    'sign.log',
    'sign.request',
    'sign.request.item',
    'sign.request.item.value',
    'sign.send.request',
    'sign.send.request.signer',
    'sign.template',
    'sign.template.tag',
    'slide.answer',
    'slide.channel',
    'slide.channel.invite',
    'slide.channel.partner',
    'slide.channel.tag',
    'slide.channel.tag.group',
    'slide.embed',
    'slide.question',
    'slide.slide',
    'slide.slide.partner',
    'slide.slide.resource',
    'slide.tag',
    'sms.composer',
    'sms.resend',
    'sms.resend.recipient',
    'sms.sms',
    'sms.template',
    'sms.template.preview',
    'sms.template.reset',
    'sms.tracker',
    'snailmail.letter',
    'snailmail.letter.format.error',
    'snailmail.letter.missing.required.fields',
    'spreadsheet.contributor',
    'spreadsheet.dashboard',
    'spreadsheet.dashboard.group',
    'spreadsheet.dashboard.share',
    'spreadsheet.document.to.dashboard',
    'spreadsheet.mixin',
    'spreadsheet.revision',
    'spreadsheet.template',
    'stock.assign.serial',
    'stock.backorder.confirmation',
    'stock.backorder.confirmation.line',
    'stock.change.product.qty',
    'stock.forecasted_product_product',
    'stock.forecasted_product_template',
    'stock.inventory.adjustment.name',
    'stock.inventory.conflict',
    'stock.inventory.warning',
    'stock.location',
    'stock.lot',
    'stock.move',
    'stock.move.line',
    'stock.orderpoint.snooze',
    'stock.package.destination',
    'stock.package.type',
    'stock.package_level',
    'stock.picking',
    'stock.picking.type',
    'stock.putaway.rule',
    'stock.quant',
    'stock.quant.package',
    'stock.quant.relocate',
    'stock.quantity.history',
    'stock.replenishment.info',
    'stock.replenishment.option',
    'stock.report',
    'stock.request.count',
    'stock.return.picking',
    'stock.return.picking.line',
    'stock.route',
    'stock.rule',
    'stock.rules.report',
    'stock.scheduler.compute',
    'stock.scrap',
    'stock.storage.category',
    'stock.storage.category.capacity',
    'stock.traceability.report',
    'stock.track.confirmation',
    'stock.track.line',
    'stock.valuation.layer',
    'stock.valuation.layer.revaluation',
    'stock.warehouse',
    'stock.warehouse.orderpoint',
    'stock.warn.insufficient.qty',
    'stock.warn.insufficient.qty.scrap',
    'survey.invite',
    'survey.question',
    'survey.question.answer',
    'survey.survey',
    'survey.user_input',
    'survey.user_input.line',
    'template.reset.mixin',
    'theme.ir.asset',
    'theme.ir.attachment',
    'theme.ir.ui.view',
    'theme.utils',
    'theme.website.menu',
    'theme.website.page',
    'uom.category',
    'uom.uom',
    'utm.campaign',
    'utm.medium',
    'utm.mixin',
    'utm.source',
    'utm.source.mixin',
    'utm.stage',
    'utm.tag',
    'validate.account.move',
    'vendor.delay.report',
    'web_editor.assets',
    'web_editor.converter.test',
    'web_editor.converter.test.sub',
    'web_tour.tour',
    'website',
    'website.configurator.feature',
    'website.controller.page',
    'website.cover_properties.mixin',
    'website.menu',
    'website.multi.mixin',
    'website.page',
    'website.published.mixin',
    'website.published.multi.mixin',
    'website.rewrite',
    'website.robots',
    'website.route',
    'website.searchable.mixin',
    'website.seo.metadata',
    'website.snippet.filter',
    'website.track',
    'website.visitor',
    'wizard.ir.model.menu.create'
]

ACCESS_RIGHTS = Literal["create", "read", "write", "unlink"]

API_METHODS = Literal["check_access_rights", "search", "search_read", "search_count", "read", "create", "write", "unlink"]