import { useEffect, useState } from 'react';
import { Pressable, ScrollView, Share, StyleSheet, Text, View } from 'react-native';
import DetailHeader, { detailTopInset } from '../components/DetailHeader';
import engage from '../lib/dailyEngage';
import { hydrateEngage } from '../lib/deviceStorage';
import { readingBlocks } from '../lib/dailyFeed';
import { shareDetail } from '../lib/shareDetail';

const BG = '#07070a';
const TEXT = '#f4f4f5';
const MUTED = '#a1a1aa';
const ACCENT = '#8b9cff';
const SHEET = '#121218';

function ActionIcon({ kind, on }) {
  const color = on ? ACCENT : MUTED;
  if (kind === 'like') {
    return <Text style={[styles.glyph, { color }]}>{on ? '♥' : '♡'}</Text>;
  }
  return <Text style={[styles.glyph, { color }]}>↑</Text>;
}

export default function DailyReader({ item, onClose }) {
  const blocks = readingBlocks(item);
  const [liked, setLiked] = useState(false);
  const [toast, setToast] = useState('');
  const [ready, setReady] = useState(false);
  const inset = detailTopInset();

  useEffect(() => {
    let live = true;
    hydrateEngage().then(function () {
      if (!live || !item) return;
      return engage.getLike(item.date).then(function (value) {
        if (!live) return;
        setLiked(value);
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
    const status = await shareDetail(title, url, function (payload) {
      return Share.share(payload);
    });
    if (status === 'copied') setToast('Link copied');
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
          <Pressable testID="reader-share-row" accessibilityRole="button" onPress={onShare} style={styles.action}>
            <ActionIcon kind="share" />
            <Text style={styles.actionLabel}>Share</Text>
          </Pressable>
        </View>
      </ScrollView>
      <DetailHeader
        onClose={onClose}
        onShare={onShare}
        closeTestID="reader-close"
        shareTestID="reader-share"
      />
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
