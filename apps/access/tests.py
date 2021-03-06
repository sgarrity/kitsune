from django.test import TestCase
from django.contrib.auth.models import User

from nose.tools import eq_
import test_utils

import access
from .helpers import has_perm, has_perm_or_owns
from sumo.urlresolvers import reverse
from forums.models import Forum, Thread


class ForumTestPermissions(TestCase):
    fixtures = ['users.json', 'posts.json', 'forums_permissions.json']

    def setUp(self):
        url = reverse('forums.threads', args=[u'test-forum'])
        self.context = {'request': test_utils.RequestFactory().get(url)}
        self.forum_1 = Forum.objects.get(pk=1)
        self.forum_2 = Forum.objects.get(pk=2)

    def test_has_perm_thread_edit(self):
        """
        User in ForumsModerator group can edit thread in forum_1, but not in
        forum_2.
        """
        self.context['request'].user = User.objects.get(pk=47963)
        allowed = has_perm(self.context, 'forums_forum.thread_edit_forum',
                           self.forum_1)
        eq_(allowed, True)
        allowed = has_perm(self.context, 'forums_forum.thread_edit_forum',
                           self.forum_2)
        eq_(allowed, False)

    def test_has_perm_or_owns_thread_edit(self):
        """
        User in ForumsModerator group can edit thread in forum_1, but not in
        forum_2.
        """
        me = User.objects.get(pk=118533)
        my_t = Thread.objects.filter(creator=me)[0]
        other_t = Thread.objects.exclude(creator=me)[0]
        self.context['request'].user = me
        perm = 'forums_forum.thread_edit_forum'
        allowed = has_perm_or_owns(self.context, perm, my_t, self.forum_1)
        eq_(allowed, True)
        allowed = has_perm_or_owns(self.context, perm, other_t, self.forum_1)
        eq_(allowed, False)

    def test_has_perm_thread_delete(self):
        """
        User in ForumsModerator group can delete thread in forum_1, but not in
        forum_2.
        """
        self.context['request'].user = User.objects.get(pk=47963)
        allowed = has_perm(self.context, 'forums_forum.thread_delete_forum',
                           self.forum_1)
        eq_(allowed, True)
        allowed = has_perm(self.context, 'forums_forum.thread_delete_forum',
                           self.forum_2)
        eq_(allowed, False)

    def test_has_perm_thread_sticky(self):
        """
        User in ForumsModerator group can change sticky status of thread in
        forum_1, but not in forum_2.
        """
        self.context['request'].user = User.objects.get(pk=47963)
        allowed = has_perm(self.context, 'forums_forum.thread_sticky_forum',
                           self.forum_1)
        eq_(allowed, True)
        allowed = has_perm(self.context, 'forums_forum.thread_sticky_forum',
                           self.forum_2)
        eq_(allowed, False)

    def test_has_perm_thread_locked(self):
        """
        Sanity check: ForumsModerator group has no permission to change locked
        status in forum_1.
        """
        self.context['request'].user = User.objects.get(pk=47963)
        allowed = has_perm(self.context, 'forums_forum.thread_locked_forum',
                           self.forum_1)
        eq_(allowed, False)

    def test_has_perm_post_edit(self):
        """
        User in ForumsModerator group can edit any post in forum_1, but not
        in forum_2.
        """
        self.context['request'].user = User.objects.get(pk=47963)
        allowed = has_perm(self.context, 'forums_forum.post_edit_forum',
                           self.forum_1)
        eq_(allowed, True)
        allowed = has_perm(self.context, 'forums_forum.post_edit_forum',
                           self.forum_2)
        eq_(allowed, False)

    def test_has_perm_post_delete(self):
        """
        User in ForumsModerator group can delete any post in forum_1, but not
        in forum_2.
        """
        self.context['request'].user = User.objects.get(pk=47963)
        allowed = has_perm(self.context, 'forums_forum.post_delete_forum',
                           self.forum_1)
        eq_(allowed, True)
        allowed = has_perm(self.context, 'forums_forum.post_delete_forum',
                           self.forum_2)
        eq_(allowed, False)

    def test_no_perm_thread_delete(self):
        """
        User not in ForumsModerator group cannot delete thread in any forum.
        """
        self.context['request'].user = User.objects.get(pk=118533)
        allowed = has_perm(self.context, 'forums_forum.thread_delete_forum',
                           self.forum_1)
        eq_(allowed, False)
        allowed = has_perm(self.context, 'forums_forum.thread_delete_forum',
                           self.forum_2)
        eq_(allowed, False)

    def test_admin_perm_thread(self):
        """Super user can do anything on any forum."""
        self.context['request'].user = User.objects.get(pk=1)

        # Loop over all forums perms and both forums
        perms = ('thread_edit_forum', 'thread_delete_forum', 'post_edit_forum',
                 'thread_sticky_forum', 'thread_locked_forum',
                 'post_delete_forum')
        forums = (self.forum_1, self.forum_2)

        for perm in perms:
            for forum in forums:
                allowed = has_perm(self.context, 'forums_forum.' + perm,
                                   forum)
                eq_(allowed, True)

    def test_util_has_perm_or_owns_sanity(self):
        """Sanity check for access.has_perm_or_owns."""
        me = User.objects.get(pk=118533)
        my_t = Thread.objects.filter(creator=me)[0]
        other_t = Thread.objects.exclude(creator=me)[0]
        perm = 'forums_forum.thread_edit_forum'
        allowed = access.has_perm_or_owns(me, perm, my_t, self.forum_1)
        eq_(allowed, True)
        allowed = access.has_perm_or_owns(me, perm, other_t, self.forum_1)
        eq_(allowed, False)

    def test_has_perm_per_object(self):
        """Assert has_perm checks per-object permissions correctly."""
        user = User.objects.get(pk=47963)
        perm = 'forums_forum.thread_edit_forum'
        assert access.has_perm(user, perm, self.forum_1)
        assert not access.has_perm(user, perm, self.forum_2)

    def test_perm_is_defined_on(self):
        """Test whether we check for permission relationship, independent of
        whether the permission is actually assigned to anyone."""
        perm = 'forums_forum.view_in_forum'
        assert access.perm_is_defined_on(perm, Forum.objects.get(pk=3))
        assert not access.perm_is_defined_on(perm, Forum.objects.get(pk=2))
