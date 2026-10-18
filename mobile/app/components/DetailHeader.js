import { useState, useEffect } from 'react';
import { Platform, Pressable, Share, StatusBar, StyleSheet, Text, View } from 'react-native';
import { shareDetail } from '../lib/shareDetail';

const TEXT = '#f4f4f5';
const SHEET = '#121218';

export function detailTopInset() {
  if (Platform.OS === 'ios') return 47;
  if (Platform.OS === 'android') return StatusBar.currentHeight || 0;
  return 0;
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

export default function DetailHeader({ onClose, onShare, title, url, closeTestID, shareTestID }) {
  const [toast, setToast] = useState('');
  const inset = detailTopInset();

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

  async function pressShare() {
    if (onShare) {
      await onShare();
      return;
    }
    const status = await shareDetail(title, url, function (payload) {
      return Share.share(payload);
    });
    if (status === 'copied') setToast('Link copied');
  }

  return (
    <View pointerEvents="box-none" style={[styles.bar, { top: inset + 8 }]}>
      <Pressable
        testID={closeTestID || 'detail-close'}
        accessibilityRole="button"
        accessibilityLabel="Close"
        onPress={onClose}
        style={styles.button}
      >
        <CloseIcon />
      </Pressable>
      <Pressable
        testID={shareTestID || 'detail-share'}
        accessibilityRole="button"
        accessibilityLabel="Share"
        onPress={pressShare}
        style={styles.button}
      >
        <ShareIcon />
      </Pressable>
      {toast ? <Text style={styles.toast}>{toast}</Text> : null}
    </View>
  );
}

const webBlur = Platform.OS === 'web'
  ? { backdropFilter: 'blur(16px)', WebkitBackdropFilter: 'blur(16px)' }
  : null;

const styles = StyleSheet.create({
  bar: {
    position: 'absolute',
    left: 0,
    right: 0,
    zIndex: 2,
    paddingHorizontal: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  button: {
    width: 44,
    height: 44,
    borderRadius: 22,
    borderWidth: 1,
    borderColor: 'rgba(244, 244, 245, 0.72)',
    backgroundColor: 'rgba(7, 7, 10, 0.46)',
    alignItems: 'center',
    justifyContent: 'center',
    ...(webBlur || {}),
  },
  iconBox: { width: 18, height: 18, alignItems: 'center', justifyContent: 'center' },
  iconBar: { position: 'absolute', width: 14, height: 1.8, backgroundColor: '#fff', borderRadius: 1 },
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
    top: 56,
    alignSelf: 'center',
    left: 0,
    right: 0,
    textAlign: 'center',
    color: TEXT,
    backgroundColor: SHEET,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.12)',
    borderRadius: 999,
    overflow: 'hidden',
    marginHorizontal: 80,
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
});
