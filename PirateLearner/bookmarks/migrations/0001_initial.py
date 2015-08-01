# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bookmark'
        db.create_table(u'bookmarks_bookmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('adder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added_bookmarks', to=orm['auth.User'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'bookmarks', ['Bookmark'])

        # Adding model 'BookmarkFolderInstance'
        db.create_table(u'bookmarks_bookmarkfolderinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('adder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bookmarks_folder', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'bookmarks', ['BookmarkFolderInstance'])

        # Adding model 'BookmarkInstance'
        db.create_table(u'bookmarks_bookmarkinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bookmark', self.gf('django.db.models.fields.related.ForeignKey')(related_name='saved_instances', to=orm['bookmarks.Bookmark'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='saved_bookmarks', to=orm['auth.User'])),
            ('saved', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('folder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.BookmarkFolderInstance'])),
            ('privacy_level', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'bookmarks', ['BookmarkInstance'])


    def backwards(self, orm):
        # Deleting model 'Bookmark'
        db.delete_table(u'bookmarks_bookmark')

        # Deleting model 'BookmarkFolderInstance'
        db.delete_table(u'bookmarks_bookmarkfolderinstance')

        # Deleting model 'BookmarkInstance'
        db.delete_table(u'bookmarks_bookmarkinstance')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bookmarks.bookmark': {
            'Meta': {'ordering': "['-added']", 'object_name': 'Bookmark'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'adder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_bookmarks'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'bookmarks.bookmarkfolderinstance': {
            'Meta': {'object_name': 'BookmarkFolderInstance'},
            'adder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookmarks_folder'", 'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'bookmarks.bookmarkinstance': {
            'Meta': {'object_name': 'BookmarkInstance'},
            'bookmark': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'saved_instances'", 'to': u"orm['bookmarks.Bookmark']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.BookmarkFolderInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'privacy_level': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'saved': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'saved_bookmarks'", 'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['bookmarks']