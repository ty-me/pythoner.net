# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Picture'
        db.delete_table('wiki_picture')

        # Adding field 'Entry.image_urls'
        db.add_column('wiki_entry', 'image_urls',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1000),
                      keep_default=False)

        # Removing M2M table for field picture on 'Entry'
        db.delete_table('wiki_entry_picture')


    def backwards(self, orm):
        # Adding model 'Picture'
        db.create_table('wiki_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('wiki', ['Picture'])

        # Deleting field 'Entry.image_urls'
        db.delete_column('wiki_entry', 'image_urls')

        # Adding M2M table for field picture on 'Entry'
        db.create_table('wiki_entry_picture', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['wiki.entry'], null=False)),
            ('picture', models.ForeignKey(orm['wiki.picture'], null=False))
        ))
        db.create_unique('wiki_entry_picture', ['entry_id', 'picture_id'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'wiki.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'wiki.entry': {
            'Meta': {'ordering': "['public', '-sub_time']", 'object_name': 'Entry'},
            'allow_comment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['wiki.Category']"}),
            'click_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_urls': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'plink': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sub_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['wiki.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'wiki.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wiki']