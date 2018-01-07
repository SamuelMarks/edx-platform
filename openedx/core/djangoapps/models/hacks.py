from tempfile import gettempdir

from os import path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_arguments('--info-for-course-id', action='store',
                             dest='course_id')

    def handle(self, *args, **options):
        if options['info-for-course-id']:
            dump_course_info(options['info-for-course-id'])


def dump_course_info(course_id):
    print 'dump_course_info(\'{}\')'.format(course_id)

    from xmodule.modulestore.django import modulestore
    from opaque_keys.edx.keys import CourseKey, UsageKey

    course_key = CourseKey.from_string(course_id)
    ms = modulestore()
    sequences = ms.get_items(course_key, qualifiers={'category': 'sequential'})

    with open(path.join(gettempdir(), '{}.hacks.log'.format(course_id))) as f:
        f.write('location\tseq.display_name\n')
        for seq in sequences:
            print seq.location, seq.display_name
            f.write('{location}\t{display_name}\n'.format(location=seq.location,
                                                          display_name=seq.display_name))
