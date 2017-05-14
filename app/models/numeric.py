import os
import datetime
from config import basedir
from flask import render_template_string
from flask_admin.contrib.mongoengine import ModelView
from .. import db, socketio
from .basecontrol import BaseControl


class Numeric(BaseControl):
    topic = db.StringField()
    icon_dir = os.path.join(basedir, 'app/static/icons')
    icons = [(x, os.path.splitext(x)[0])
             for x in os.listdir(icon_dir) if x[-3:].lower() == 'png']
    icon = db.StringField(choices=icons)
    precision = db.IntField(min_value=0, max_value=6, default=2)
    suffix = db.StringField(max_length=8)

    _update_time = db.DateTimeField()
    _value = db.DecimalField()

    @property
    def value(self):
        return round(self._value, self.precision)

    @value.setter
    def value(self, val):
        self._value = val
        self._update_time = datetime.datetime.now()

    def __str__(self):
        return self.name

    def render_html(self):
        return render_template_string(
            '<div class="form-group" id="control{{ control.id }}" title="last updated: {{ control._update_time | strftime }}">'
            '  <label class="control-label item-label col-xs-6">'
            '    {% if control.icon %}'
            '    <img class="icon" src="{{ url_for("static", filename="icons/" + control.icon) }}">'
            '    {% endif %}'
            '    {{ control.label }}:'
            '  </label>'
            '  <div class="col-sm-6 col-xs-6">'
            '    <div class="input-group">'
            '      <input class="form-control mqtt-item-value" readonly value={{ control.value }}>'
            '      <span class="input-group-addon">{{ control.suffix }}</span>'
            '    </div>'
            '  </div>'
            '</div>', control=self)

    def render_js(self):
        return render_template_string(
            'socket.on("mqtt_message_{{ control.id }}", function(data) {\n'
            '  $row = $("#control" + "{{ control.id }}")\n'
            '  $row.prop("title", data.update_time);\n'
            '  $row.find(".mqtt-item-value").val(data.value);\n'
            '});\n', control=self
        )

    def handle_event(self, data):
        pass

    def handle_mqtt_message(self, client, userdata, message):
        self.value = float(message.payload)
        self.save()
        socketio.emit(
            'mqtt_message_{}'.format(self.id),
            dict(
                id=str(self.id), value=self.value,
                update_time=self._update_time.strftime(
                    'last updated: %d.%m.%Y %H:%M:%S')
            )
        )

    def get_subscribed_topics(self):
        return [self.topic]
