# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Messages'
        db.create_table(u'thread_messages_messages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='message_sender', to=orm['auth.User'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thread_messages.Messages'], null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'thread_messages', ['Messages'])

        # Adding model 'Thread'
        db.create_table(u'thread_messages_thread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='last_message_in_thread', to=orm['thread_messages.Messages'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'thread_messages', ['Thread'])

        # Adding M2M table for field participants on 'Thread'
        m2m_table_name = db.shorten_name(u'thread_messages_thread_participants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thread', models.ForeignKey(orm[u'thread_messages.thread'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thread_id', 'user_id'])

        # Adding M2M table for field messages on 'Thread'
        m2m_table_name = db.shorten_name(u'thread_messages_thread_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thread', models.ForeignKey(orm[u'thread_messages.thread'], null=False)),
            ('messages', models.ForeignKey(orm[u'thread_messages.messages'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thread_id', 'messages_id'])

        # Adding model 'ParticipantThreads'
        db.create_table(u'thread_messages_participantthreads', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='thread_participant', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'thread_messages', ['ParticipantThreads'])

        # Adding M2M table for field threads on 'ParticipantThreads'
        m2m_table_name = db.shorten_name(u'thread_messages_participantthreads_threads')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantthreads', models.ForeignKey(orm[u'thread_messages.participantthreads'], null=False)),
            ('thread', models.ForeignKey(orm[u'thread_messages.thread'], null=False))
        ))
        db.create_unique(m2m_table_name, ['participantthreads_id', 'thread_id'])

        # Adding model 'ParticipantNotifications'
        db.create_table(u'thread_messages_participantnotifications', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notified_participant', to=orm['auth.User'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participant_thread', to=orm['thread_messages.Thread'])),
            ('message_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'thread_messages', ['ParticipantNotifications'])


    def backwards(self, orm):
        # Deleting model 'Messages'
        db.delete_table(u'thread_messages_messages')

        # Deleting model 'Thread'
        db.delete_table(u'thread_messages_thread')

        # Removing M2M table for field participants on 'Thread'
        db.delete_table(db.shorten_name(u'thread_messages_thread_participants'))

        # Removing M2M table for field messages on 'Thread'
        db.delete_table(db.shorten_name(u'thread_messages_thread_messages'))

        # Deleting model 'ParticipantThreads'
        db.delete_table(u'thread_messages_participantthreads')

        # Removing M2M table for field threads on 'ParticipantThreads'
        db.delete_table(db.shorten_name(u'thread_messages_participantthreads_threads'))

        # Deleting model 'ParticipantNotifications'
        db.delete_table(u'thread_messages_participantnotifications')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'thread_messages.messages': {
            'Meta': {'object_name': 'Messages'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['thread_messages.Messages']", 'null': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'message_sender'", 'to': u"orm['auth.User']"})
        },
        u'thread_messages.participantnotifications': {
            'Meta': {'object_name': 'ParticipantNotifications'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notified_participant'", 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participant_thread'", 'to': u"orm['thread_messages.Thread']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'thread_messages.participantthreads': {
            'Meta': {'object_name': 'ParticipantThreads'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'thread_participant'", 'to': u"orm['auth.User']"}),
            'threads': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participant_threads'", 'symmetrical': 'False', 'to': u"orm['thread_messages.Thread']"})
        },
        u'thread_messages.thread': {
            'Meta': {'object_name': 'Thread'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_message_in_thread'", 'to': u"orm['thread_messages.Messages']"}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'thread_messages'", 'symmetrical': 'False', 'to': u"orm['thread_messages.Messages']"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'thread_participants'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['thread_messages']