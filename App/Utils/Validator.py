#
# Validator
#

from flask import flash, url_for, redirect


class Validator():
    errors = []

    def required(self, form, fields):
        for field in fields:
            if (form[field] is None):
                self.errors.append(f"{field} Wajib Di isi")
                pass
        pass
        return self
    pass

    def flashMessage(self):
        if len(self.errors) > 0:
            flash(self.errors[0], 'danger')
        return self
    pass

    def redirect(self, target):
        return redirect(url_for(target))
    pass


pass
