#Updates comment count for parent posts
def update_comment_counts(parent, action):
    if parent:
        if action == 'add':
            parent.comment_count += 1
        if action == 'delete':
            parent.comment_count -= 1
        parent.save()
        return update_comment_counts(parent.parent, action)

#Gets triggered on post created and updates remumble count if shared or deleted
def update_remumble_counts(parent, action):

    if action == 'add':

        parent.share_count += 1

    if action == 'delete':
        parent.share_count -= 1

    parent.save()
