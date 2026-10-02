import { useEffect, useState } from 'react';
import { Dimensions, Platform, Pressable, ScrollView, Share, StyleSheet, Text, TextInput, View } from 'react-native';
import engage from '../lib/dailyEngage';
import { hydrateEngage } from '../lib/deviceStorage';
import { readingBlocks } from '../lib/dailyFeed';

const BG = '#07070a';
const TEXT = '#f4f4f5';
const MUTED = '#a1a1aa';
const ACCENT = '#8b9cff';
const SHEET = '#121218';

function topInset() {
  return Platform.OS === 'ios' ? 47 : 0;
}

function CloseIcon() {
  return (
    <View style={styles.iconBox}>
      <View style={[styles.iconBar, { transform: [{ rotate: '45deg' }] }]} />
      <View style={[styles.iconBar, { transform: [{ rotate: '-45deg' }] }]} />
    </View>
  );
}

function ShareIcon() {
  return (
    <View style={styles.shareIcon}>
      <View style={styles.shareStem} />
      <View style={styles.shareHead} />
      <View style={styles.shareBox} />
    </View>
  );
}

function ActionIcon({ kind, on }) {
  const color = on ? ACCENT : MUTED;
  if (kind === 'like') {
    return <Text style={[styles.glyph, { color }]}>{on ? '♥' : '♡'}</Text>;
  }
  if (kind === 'comment') {
    return <View style={[styles.bubble, { borderColor: color }]} />;
  }
  return <Text style={[styles.glyph, { color }]}>↑</Text>;
}

export default function DailyReader({ item, onClose }) {
  const blocks = readingBlocks(item);
  const question = item && String(item.discussionQuestion || '').trim();
  const [liked, setLiked] = useState(false);
  const [comments, setComments] = useState([]);
  const [sheet, setSheet] = useState(false);
  const [name, setName] = useState('');
  const [text, setText] = useState('');
  const [status, setStatus] = useState('');
  const [toast, setToast] = useState('');
  const [ready, setReady] = useState(false);
  const inset = topInset();

  useEffect(() => {
    let live = true;
    hydrateEngage().then(function () {
      if (!live || !item) return;
      return Promise.all([
        engage.getLike(item.date),
        engage.getComments(item.date),
        engage.getDisplayName(),
      ]).then(function (result) {
        if (!live) return;
        setLiked(result[0]);
        setComments(result[1]);
        setName(result[2] || '');
        setReady(true);
      });
    }).catch(function () {
      if (live) setReady(true);
    });
    return function () { live = false; };
  }, [item]);

  useEffect(() => {
    if (!toast) return undefined;
    const timer = setTimeout(function () { setToast(''); }, 1600);
    return function () { clearTimeout(timer); };
  }, [toast]);

  useEffect(() => {
    if (Platform.OS !== 'web' || typeof document === 'undefined') return undefined;
    function onKey(event) {
      if (event.key !== 'Escape') return;
      if (sheet) setSheet(false);
      else if (onClose) onClose();
    }
    document.addEventListener('keydown', onKey);
    return function () { document.removeEventListener('keydown', onKey); };
  }, [sheet, onClose]);

  async function toggleLike() {
    if (!ready || !item) return;
    const next = !liked;
    const saved = await engage.setLike(item.date, next);
    setLiked(saved);
  }

  async function onShare() {
    if (!item) return;
    const url = engage.buildDailyShareUrl('https://www.walksteadfast.com', item.date);
    const title = item.silentTitle || item.title || 'Daily Walk';
    try {
      await Share.share({ title: title, message: title + '\n' + url, url: url });
    } catch (err) {
      if (err && err.name === 'AbortError') return;
      try {
        if (typeof navigator !== 'undefined' && navigator.clipboard) {
          await navigator.clipboard.writeText(url);
          setToast('Link copied');
        }
      } catch (copyErr) {}
    }
  }

  async function postComment() {
    if (!item) return;
    if (!String(name).trim() || !String(text).trim()) {
      setStatus('Add your name and a comment.');
      return;
    }
    await engage.setDisplayName(name);
    await engage.addComment(item.date, { name: name, text: text });
    setComments(await engage.getComments(item.date));
    setText('');
    setStatus('Saved on this device.');
  }

  async function report(id) {
    if (!item) return;
    await engage.reportComment(item.date, id);
    setComments(await engage.getComments(item.date));
    setStatus('Report saved on this device.');
  }

  return (
    <View style={styles.reader}>
      <ScrollView
        testID="reader-scroll"
        style={styles.scroll}
        contentContainerStyle={[styles.measure, { paddingTop: 78 + inset }]}
      >
        {blocks.map(function (para, index) {
          return <Text key={index} style={styles.para}>{para}</Text>;
        })}
        <View style={styles.actions}>
          <Pressable testID="reader-like" accessibilityRole="button" accessibilityState={{ selected: liked }} onPress={toggleLike} style={styles.action}>
            <ActionIcon kind="like" on={liked} />
            <Text style={[styles.actionLabel, liked && styles.actionOn]}>Like</Text>
          </Pressable>
          <Pressable testID="reader-comment" accessibilityRole="button" onPress={function () { setStatus(''); setSheet(true); }} style={styles.action}>
            <ActionIcon kind="comment" />
            <Text style={styles.actionLabel}>Comment</Text>
          </Pressable>
          <Pressable testID="reader-share-row" accessibilityRole="button" onPress={onShare} style={styles.action}>
            <ActionIcon kind="share" />
            <Text style={styles.actionLabel}>Share</Text>
          </Pressable>
        </View>
      </ScrollView>
      <View pointerEvents="none" style={[styles.scrim, { height: 90 + inset }]}>
        <View style={[styles.scrimBand, { flex: 2, backgroundColor: BG }]} />
        <View style={[styles.scrimBand, { backgroundColor: 'rgba(7,7,10,0.82)' }]} />
        <View style={[styles.scrimBand, { backgroundColor: 'rgba(7,7,10,0.45)' }]} />
        <View style={[styles.scrimBand, { backgroundColor: 'rgba(7,7,10,0)' }]} />
      </View>
      <Pressable
        testID="reader-close"
        accessibilityRole="button"
        accessibilityLabel="Close"
        onPress={onClose}
        style={[styles.round, { top: 10 + inset, left: 16 }]}
      >
        <CloseIcon />
      </Pressable>
      <Pressable
        testID="reader-share"
        accessibilityRole="button"
        accessibilityLabel="Share"
        onPress={onShare}
        style={[styles.round, { top: 10 + inset, right: 16 }]}
      >
        <ShareIcon />
      </Pressable>
      {sheet ? (
        <View style={styles.sheetLayer}>
          <Pressable style={styles.sheetBackdrop} onPress={function () { setSheet(false); }} accessibilityLabel="Close comments" />
          <View testID="comment-sheet" style={[styles.sheet, { maxHeight: Math.round(Dimensions.get('window').height * 0.86) }]}>
            <View style={styles.sheetHead}>
              <Text style={styles.sheetTitle}>Comments</Text>
              <Pressable accessibilityRole="button" accessibilityLabel="Close comments" onPress={function () { setSheet(false); }} style={styles.dismiss}>
                <CloseIcon />
              </Pressable>
            </View>
            <Text style={styles.help}>Public comments are coming soon. For now, comments stay on this device.</Text>
            <ScrollView style={styles.commentList}>
              {question ? (
                <View testID="discussion-question" style={styles.pinned}>
                  <View style={styles.meta}>
                    <Text style={styles.commentName}>Steadfast Team</Text>
                    <Text style={styles.badge}>Team</Text>
                  </View>
                  <Text style={styles.commentText}>{question}</Text>
                </View>
              ) : null}
              {comments.length === 0 ? (
                <Text testID="comment-empty" style={styles.empty}>Be the first to comment.</Text>
              ) : comments.map(function (comment) {
                const when = engage.formatRelativeTime(comment.createdAt, Date.now());
                return (
                  <View key={comment.id} style={styles.userComment}>
                    <View style={styles.meta}>
                      <Text style={styles.commentName}>{comment.name}</Text>
                      <Text style={styles.when}>{when}</Text>
                    </View>
                    <Text style={styles.commentText}>{comment.text}</Text>
                    <Pressable
                      accessibilityRole="button"
                      accessibilityLabel="Report"
                      disabled={comment.reported}
                      onPress={function () { report(comment.id); }}
                    >
                      <Text style={styles.report}>{comment.reported ? 'Reported' : 'Report'}</Text>
                    </Pressable>
                  </View>
                );
              })}
            </ScrollView>
            <Text style={styles.fieldLabel}>Name</Text>
            <TextInput
              testID="comment-name"
              value={name}
              onChangeText={setName}
              maxLength={40}
              autoComplete="nickname"
              style={styles.input}
            />
            <Text style={styles.fieldLabel}>Comment</Text>
            <TextInput
              testID="comment-text"
              value={text}
              onChangeText={setText}
              maxLength={500}
              multiline
              style={[styles.input, styles.area]}
            />
            {status ? <Text style={styles.status}>{status}</Text> : null}
            <Pressable testID="comment-post" accessibilityRole="button" onPress={postComment} style={styles.post}>
              <Text style={styles.postText}>Post</Text>
            </Pressable>
          </View>
        </View>
      ) : null}
      {toast ? <Text style={styles.toast}>{toast}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  reader: { flex: 1, backgroundColor: BG },
  scroll: { flex: 1 },
  measure: { paddingHorizontal: 22, paddingBottom: 48 },
  para: { color: TEXT, fontSize: 17, lineHeight: 26, marginBottom: 24, textAlign: 'left' },
  actions: {
    marginTop: 16,
    paddingTop: 18,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255,255,255,0.08)',
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  action: { minHeight: 44, flexDirection: 'row', alignItems: 'center', gap: 8 },
  actionLabel: { color: MUTED, fontSize: 15, fontWeight: '500' },
  actionOn: { color: ACCENT },
  glyph: { fontSize: 18, color: MUTED },
  bubble: { width: 18, height: 14, borderWidth: 1.6, borderRadius: 3 },
  scrim: { position: 'absolute', top: 0, left: 0, right: 0 },
  scrimBand: { flex: 1 },
  round: {
    position: 'absolute',
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(60,60,64,0.75)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconBox: { width: 18, height: 18, alignItems: 'center', justifyContent: 'center' },
  iconBar: { position: 'absolute', width: 16, height: 1.8, backgroundColor: '#fff' },
  shareIcon: { width: 16, height: 18, alignItems: 'center' },
  shareStem: { position: 'absolute', top: 2, width: 1.8, height: 8, backgroundColor: '#fff' },
  shareHead: {
    position: 'absolute',
    top: 1,
    width: 8,
    height: 8,
    borderTopWidth: 1.8,
    borderRightWidth: 1.8,
    borderColor: '#fff',
    transform: [{ rotate: '-45deg' }],
  },
  shareBox: {
    position: 'absolute',
    bottom: 0,
    width: 14,
    height: 9,
    borderWidth: 1.8,
    borderTopWidth: 0,
    borderColor: '#fff',
  },
  sheetLayer: { position: 'absolute', top: 0, right: 0, bottom: 0, left: 0, justifyContent: 'flex-end' },
  sheetBackdrop: { position: 'absolute', top: 0, right: 0, bottom: 0, left: 0, backgroundColor: 'rgba(0,0,0,0.55)' },
  sheet: {
    backgroundColor: SHEET,
    borderTopLeftRadius: 18,
    borderTopRightRadius: 18,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    paddingHorizontal: 18,
    paddingTop: 12,
    paddingBottom: 16,
  },
  sheetHead: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  sheetTitle: { color: TEXT, fontSize: 20, fontWeight: '500' },
  dismiss: { width: 44, height: 44, alignItems: 'center', justifyContent: 'center' },
  help: { color: MUTED, fontSize: 14, lineHeight: 20, marginBottom: 12 },
  commentList: { flexGrow: 0, maxHeight: 220, marginBottom: 8 },
  pinned: { paddingBottom: 12 },
  userComment: { paddingVertical: 12, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.08)' },
  meta: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  commentName: { color: TEXT, fontSize: 14, fontWeight: '600' },
  badge: {
    color: BG,
    backgroundColor: ACCENT,
    overflow: 'hidden',
    borderRadius: 999,
    paddingHorizontal: 6,
    paddingVertical: 1,
    fontSize: 11,
    fontWeight: '600',
  },
  when: { color: MUTED, fontSize: 13 },
  commentText: { color: TEXT, fontSize: 15, lineHeight: 22, marginTop: 4 },
  empty: { color: MUTED, fontSize: 15, marginBottom: 8 },
  report: { color: MUTED, fontSize: 13, textDecorationLine: 'underline', marginTop: 6 },
  fieldLabel: { color: MUTED, fontSize: 13, marginTop: 8 },
  input: {
    marginTop: 6,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.12)',
    borderRadius: 12,
    backgroundColor: BG,
    color: TEXT,
    fontSize: 16,
    paddingHorizontal: 12,
    paddingVertical: 10,
    minHeight: 44,
  },
  area: { minHeight: 88, textAlignVertical: 'top' },
  status: { color: MUTED, fontSize: 14, marginTop: 8 },
  post: {
    marginTop: 12,
    alignSelf: 'flex-start',
    backgroundColor: ACCENT,
    borderRadius: 999,
    minHeight: 44,
    paddingHorizontal: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  postText: { color: BG, fontSize: 15, fontWeight: '500' },
  toast: {
    position: 'absolute',
    bottom: 24,
    alignSelf: 'center',
    backgroundColor: SHEET,
    color: TEXT,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.12)',
    borderRadius: 999,
    paddingHorizontal: 14,
    paddingVertical: 10,
    overflow: 'hidden',
  },
});
