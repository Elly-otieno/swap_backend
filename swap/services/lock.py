def lock_session(session, reason):
    session.is_locked = True
    session.stage = "LOCKED"
    session.save()
