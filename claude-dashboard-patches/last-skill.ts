import { open, stat } from 'fs/promises';
import type { Widget } from './base.js';
import type { WidgetContext } from '../types.js';
import { colorize, getTheme } from '../utils/colors.js';

interface LastSkillData {
  name: string;
}

const CHUNK = 256 * 1024;

export const lastSkillWidget: Widget<LastSkillData> = {
  id: 'lastSkill',
  name: 'Last Skill',

  async getData(ctx: WidgetContext): Promise<LastSkillData | null> {
    const transcriptPath = ctx.stdin.transcript_path;
    if (!transcriptPath) return null;

    try {
      const fileStat = await stat(transcriptPath);
      const size = Math.min(CHUNK, fileStat.size);
      const fd = await open(transcriptPath, 'r');
      try {
        const buffer = Buffer.alloc(size);
        await fd.read(buffer, 0, size, fileStat.size - size);
        const lines = buffer.toString('utf-8').split('\n');

        for (let i = lines.length - 1; i >= 0; i--) {
          if (!lines[i]) continue;
          try {
            const entry = JSON.parse(lines[i]);
            const content = entry.message?.content;
            if (!Array.isArray(content)) continue;
            for (const block of content) {
              if (block.type === 'tool_use' && block.name === 'Skill' && block.input?.skill) {
                const skillName = (block.input.skill as string).split(':').pop() || block.input.skill;
                return { name: skillName };
              }
            }
          } catch { /* skip malformed lines */ }
        }
      } finally {
        await fd.close();
      }
    } catch { /* file not found or unreadable */ }

    return null;
  },

  render(data: LastSkillData, _ctx: WidgetContext): string {
    return colorize(`skill:${data.name}`, getTheme().accent);
  },
};
