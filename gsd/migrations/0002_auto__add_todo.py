# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Todo'
        db.create_table('gsd_todo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('gsd', ['Todo'])

        # Adding M2M table for field tags on 'Todo'
        db.create_table('gsd_todo_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('todo', models.ForeignKey(orm['gsd.todo'], null=False)),
            ('tag', models.ForeignKey(orm['gsd.tag'], null=False))
        ))
        db.create_unique('gsd_todo_tags', ['todo_id', 'tag_id'])


    def backwards(self, orm):
        
        # Deleting model 'Todo'
        db.delete_table('gsd_todo')

        # Removing M2M table for field tags on 'Todo'
        db.delete_table('gsd_todo_tags')


    models = {
        'gsd.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'gsd.todo': {
            'Meta': {'object_name': 'Todo'},
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gsd.Tag']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gsd']
