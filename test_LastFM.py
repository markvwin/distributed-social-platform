import LastFM as fm


def test_api_request_success():
    fm_instance = fm.LastFM()
    fm_instance.load_data()


def test_fm_transclusion():
    fm_instance = fm.LastFM()
    fm_instance.load_data()
    message = 'fm test: @lastfm'
    transcluded_message = fm_instance.transclude(message)
    assert transcluded_message != message


def test_fm_attributes_are_loaded():
    fm_instance = fm.LastFM()
    fm_instance.load_data()
    assert fm_instance.top_artist is not None
