
    @app.route('/langs')
    def langs():
        languages = db.session().query(Languages).all()
        result = ", ".join([l.language_lang for l in languages])
        if not languages:
            result = "no languages defined"
        return result

    @app.route('/langs/add/<newlang>')
    def addlang(newlang):
        if newlang in langs():
            return 'Failed to add language ' + newlang + ' because it already exists.'
        app.logger.info('Adding language '+newlang)
        l = Languages(language_lang=newlang)
        app.logger.info('Language creaeted:', l)
        db.session().add(l)
        db.session().commit()
        return langs()
