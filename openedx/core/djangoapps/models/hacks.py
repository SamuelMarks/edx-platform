from tempfile import gettempdir

from os import path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_arguments('--info-for-org', action='store',
                             dest='org')
        parser.add_arguments('--info-for-course-id', action='store',
                             dest='course_id')
        parser.add_arguments('--info-for-course-run', action='store',
                             dest='course_run')

    def handle(self, *args, **options):
        if options['course_id']:
            dump_course_info(options['org'], options['course_id'], options['course_run'])


def dump_course_info(org, course_id, run):
    print 'hacks::dump_course_info(\'{}\', \'{}\', \'{}\')'.format(org, course_id, run)

    from xmodule.modulestore.django import modulestore
    from opaque_keys.edx.keys import CourseKey, UsageKey
    from opaque_keys.edx.locator import CourseLocator

    course_str = 'course-v1:{org}+{course_id}+{run}'.format(org=org, course_id=course_id, run=run)

    course_key = CourseKey.from_string(course_str)
    # course_key = CourseLocator.from_string(course_str)
    ms = modulestore()
    sequences = ms.get_items(course_key, qualifiers={'category': 'sequential'})

    with open(path.join(gettempdir(), '{}.hacks.log'.format(course_id))) as f:
        f.write('location\tseq.display_name\n')
        for seq in sequences:
            print seq.location, seq.display_name
            f.write('{location}\t{display_name}\n'.format(location=seq.location,
                                                          display_name=seq.display_name))
