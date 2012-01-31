# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Context'
        db.create_table('gsd_context', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('color', self.gf('django.db.models.fields.CharField')(default='e9e9e9', max_length=6)),
        ))
        db.send_create_signal('gsd', ['Context'])

        # Adding field 'Todo.context'
        db.add_column('gsd_todo', 'context', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gsd.Context'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Context'
        db.delete_table('gsd_context')

        # Deleting field 'Todo.context'
        db.delete_column('gsd_todo', 'context_id')


    models = {
        'gsd.context': {
            'Meta': {'ordering': "['name']", 'object_name': 'Context'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'e9e9e9'", 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gsd.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'gsd.todo': {
            'Meta': {'ordering': "['due_date', 'context', 'name']", 'object_name': 'Todo'},
            'context': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gsd.Context']", 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gsd.Tag']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gsd']
