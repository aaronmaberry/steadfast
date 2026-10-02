import { useEffect, useState } from 'react';
import { Platform, Pressable, ScrollView, Share, StyleSheet, Text, View } from 'react-native';
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
  return <Text style={[styles.glyph, { color }]}>↑</Text>;
}

export default function DailyReader({ item, onClose }) {
  const blocks = readingBlocks(item);
  const [liked, setLiked] = useState(false);
  const [toast, setToast] = useState('');
  const [ready, setReady] = useState(false);
  const inset = topInset();

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

  useEffect(() => {
    if (Platform.OS !== 'web' || typeof document === 'undefined') return undefined;
    function onKey(event) {
      if (event.key !== 'Escape') return;
      if (onClose) onClose();
    }
    document.addEventListener('keydown', onKey);
    return function () { document.removeEventListener('keydown', onKey); };
  }, [onClose]);

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
